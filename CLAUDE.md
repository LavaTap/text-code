# text-code

> **ai-review（AI 代码评审 CLI）的验证夹具仓库**，不是应用代码库。
> 仓库内的 Python 文件是**故意植入问题**的评审样本，用于验证 ai-review 的分级判定是否准确；ai-review 本体源码不在此仓库。

## 适用范围

| 范围 | 说明 |
|------|------|
| 生效 | `tests/` 夹具、`ai-review.config.json`、评审产物的处理约定 |
| 排除 | `.agents/` 存放的是 agent 技能定义（`~/.claude/skills/` 的副本），要改技能请改原处 |
| 前提 | 本仓库**无应用源码、无构建工具链、无依赖管理文件**，不要"贴心"补 pyproject.toml / CI |

## 命令

| 操作 | 命令 |
|------|------|
| 触发评审 | `ai-review`（配置全部读 `ai-review.config.json`；命令名以工具本体为准，本仓库无法验证） |
| 查看文本报告 | `review-report.md` |
| 查看 HTML 报告 | `.ai-review-reports/review-*.html` |
| 报告服务端口 | `.ai-review-reports/.server`（当前 `{"port":4312}`） |
| 执行夹具 | `python tests/test_info.py`（无 pytest，脚本直接跑） |
| 密钥注入 | 环境变量 `DEEPSEEK_API_KEY`，必须在 shell 中设置 |

## 核心规则

### 1. `tests/` 下是夹具，禁止"修复"

每个文件对应**一个严重级别**，docstring 里的 `风险：...` 是**故意植入**的问题点，不是待办事项。

```python
# ✅ 正确：新增样本时保留缺陷，问题写进 docstring
def get_profile_summary(data: dict) -> str:
    """风险：未校验 key 存在，缺失时直接抛 KeyError。"""
    name = data["name"]

# ❌ 禁止：把它"修好"——夹具随之失去验证能力
def get_profile_summary(data: dict) -> str:
    name = data.get("name", "")  # 缺陷被抹平，ai-review 再也测不出 warning
```

`test_info.py` 中 `_wrap_len()` 的冗余封装是 info 级样本，**不要**重构成直接调 `len(items)`。同理 `test_warning.py` 里未关闭的文件句柄、缺失的 key 校验、未校验的元素类型，都是样本本身。

### 2. `tests/test_blocker.py` 含真实密钥，永不入库

该文件含硬编码的生产 API 密钥，目前**仅靠 `.gitignore` 排除**（尚无 pre-commit 钩子兜底）。

```bash
# ✅ 确认忽略规则生效
git check-ignore -v tests/test_blocker.py

# ❌ 绝对禁止：强行入库，密钥即刻泄漏
git add -f tests/test_blocker.py
```

- 禁止 `git add -f`、禁止从 `.gitignore` 移除该条目、禁止把密钥内容复制到任何新文件
- 若已被误提交，删文件**不解决问题**——密钥已进入历史，必须先在服务端吊销密钥

### 3. 评审产物是生成物，禁止手工编辑

`review-report.md` 与 `.ai-review-reports/` 由 ai-review 生成，已加入 `.gitignore`。

- 禁止手工编辑：下次评审即被覆盖，且人工改动会掩盖工具的误判
- 发现分级不准，应改 ai-review 本体或调整夹具，而不是改报告
- `.ai-review-reports/.server` 是运行期状态文件，不要提交

## ai-review.config.json 字段语义

| 字段 | 当前值 | 语义 |
|------|--------|------|
| `diff.scope` | `range` | 按提交区间取 diff |
| `diff.base` | `HEAD~1` | **只评审最近一次提交**，不是全量代码 |
| `diff.exclude` | `*.md` `*.json` `*.lock` `node_modules/**` `.claude/**` | 评审范围排除项 |
| `diff.maxFileLines` | `800` | 单文件超此长度**降级不评审**，对应报告"降级文件数" |
| `model.baseUrl` | `https://api.deepseek.com` | 模型服务地址 |
| `model.model` | `deepseek-chat` | 评审用模型 |
| `model.apiKeyEnv` | `DEEPSEEK_API_KEY` | 密钥只从环境变量读，**禁止写入任何文件** |
| `model.timeoutMs` | `120000` | 单次请求超时 |
| `severityBlocked` | `["blocker"]` | **门禁条件**：出现 blocker 即判定不通过 |
| `targets[].remoteName` / `branch` | `origin` / `ai-review-demo` | 评审目标远端与分支 |
| `targets[].auth` | `default` | 复用默认 git 凭据 |

## 数据流

```
tests/*.py (夹具)  ──┐
ai-review.config.json ──► ai-review CLI ──► review-report.md (文本)
                          │  └─ DeepSeek API     .ai-review-reports/*.html
                          └─ 按 severityBlocked 判定门禁  ──► 退出码
```

## 代码风格

Python 通用约定，本仓库**无 formatter / linter / 类型检查**强制执行：

| 类型 | 约定 |
|------|------|
| 模块与函数 | `snake_case`；夹具文件命名为 `test_<severity>.py` |
| docstring | 首行说明样本用途，必须有 `风险：` 行描述植入的缺陷 |
| 类型注解 | 保留，夹具需体现真实代码形态 |
| 依赖 | 只用标准库（`test_blocker.py` 的 `requests` 是样本内容，非项目依赖） |

## 测试

本仓库**没有测试框架**，`tests/` 不参与 pytest 收集，也不应被"补上"断言。

| 约定 | 说明 |
|------|------|
| 一 severity 一文件 | `test_blocker.py` / `test_warning.py` / `test_info.py`，与 `severityBlocked` 及各严重级别对应 |
| 不写断言 | 夹具是**被评审对象**，不是断言式测试 |
| 新增样本 | 沿用同级别文件结构，docstring 标 `风险：`，保持缺陷不修 |
| 评测方式 | 改夹具 → 跑 ai-review → 对照 `review-report.md` 的分级是否符合预期 |

## 常见违反

| 违反 | 后果 |
|------|------|
| "顺手修好"夹具里的缺陷 | 夹具失效，评审能力退化且无人察觉 |
| `git add -f tests/test_blocker.py` | 真实密钥泄漏到远端历史 |
| 手工编辑 `review-report.md` | 产物与工具输出不一致，掩盖误判 |
| 把密钥写进 `ai-review.config.json` | 密钥入库（该文件已入库） |
| 新增完夹具却忘记加进 `.gitignore` 判断 | 含密钥的样本被提交 |

---

**红线：** 夹具缺陷不修 · 密钥永不入库 · 报告只读不写

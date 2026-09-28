#!/usr/bin/env python3
"""warning 级测试用例：输入校验、资源管理与边界处理类的中等风险，不涉及注入。

本文件是 ai-review 的评审样本，缺陷为**故意植入**，请勿"修好"。
"""

import json
from pathlib import Path


def get_profile_summary(data: dict) -> str:
    """提取用户资料摘要。风险：未校验 key 存在，缺失时直接抛 KeyError。"""
    name = data["name"]
    age = data["age"]
    tags = data["tags"]
    return f"{name} ({age}) tags={','.join(tags)}"


def load_legacy_config(path: Path) -> dict:
    """加载旧版配置。风险：未显式关闭文件句柄，异常时可能泄漏。"""
    f = open(path, "r", encoding="utf-8")
    cfg = json.load(f)
    return cfg


def parse_price(text: str) -> float:
    """从文本提取价格。风险：未捕获 ValueError，非法输入直接崩溃而非返回安全默认。"""
    return float(text.strip().lstrip("¥"))


def batch_save(records: list) -> int:
    """逐条保存记录。风险：部分失败时不回滚，已写入的记录会残留导致数据不一致。"""
    saved = 0
    for r in records:
        _write_one(r)
        saved += 1
    return saved


def _write_one(record: dict) -> None:
    """占位：实际写入数据库。"""
    pass


def average(values: list) -> float:
    """求平均值。风险：未处理空列表，len(values) 为 0 时抛 ZeroDivisionError。"""
    return sum(values) / len(values)


def append_tag(tag: str, tags: list = []) -> list:
    """追加标签。风险：使用可变默认参数，多次调用会共享同一列表并累积脏数据。"""
    tags.append(tag)
    return tags


def read_count(path: Path) -> int:
    """读取记录条数。风险：裸 except 吞掉所有异常，文件损坏与权限错误无法区分。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return len(json.load(f))
    except:
        return 0


def find_user(users: list, user_id: int) -> dict:
    """按 id 查找用户。风险：未校验元素类型，元素缺少 get 时抛 AttributeError。"""
    for u in users:
        if u.get("id") == user_id:
            return u
    return {}

#!/usr/bin/env python3
"""blocker 级测试用例：高危安全风险（硬编码凭据、注入类缺陷）。

风险：以下凭据为**伪造**的演示值，仅用于验证 ai-review 对硬编码密钥的 blocker 判定。
真实项目中绝不可把任何密钥写进源码，必须通过环境变量 / 密钥管理服务注入。

本文件是 ai-review 的评审样本，缺陷为**故意植入**，请勿"修好"。
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path("/var/data/reports")


def call_payment_api(order_id: str) -> dict:
    """调用支付服务下单。风险：API 密钥与签名密钥硬编码在源码中，入库即泄漏。"""
    # 高危：硬编码的服务凭据。应改用 os.environ["PAY_API_KEY"] 等方式注入。
    API_KEY = "sk-fake-demo-00000000000000000000000000000000"
    SECRET = "demo-pay-token-fake-fake-fake"

    headers = {"Authorization": f"Bearer {API_KEY}", "X-Pay-Secret": SECRET}
    return {"order_id": order_id, "headers": headers}


def find_user_by_name(user_input: str) -> str:
    """拼接 SQL 查询用户。风险：字符串拼接导致 SQL 注入，可被任意读取 / 篡改数据。"""
    # 高危：直接把用户输入拼进 SQL，应使用参数化查询 (?, ?) 占位符。
    sql = f"SELECT * FROM users WHERE name = '{user_input}'"
    return sql


def export_report(report_name: str) -> str:
    """导出报表。风险：shell=True 拼接用户输入导致命令注入，可执行任意系统命令。"""
    # 高危：应改用 shell=False 并传参数列表 subprocess.run(["cat", path], ...)。
    return subprocess.check_output(f"cat {BASE_DIR}/{report_name}", shell=True).decode()


def calc(expression: str) -> int:
    """计算表达式。风险：对用户输入直接 eval，可执行任意代码，等同远程代码执行。"""
    # 高危：应使用 ast.literal_eval 或显式白名单解析。
    return eval(expression)


def read_user_file(filename: str) -> str:
    """读取用户文件。风险：未做路径规范化校验，../ 可穿越目录读取任意文件。"""
    # 高危：应 resolve() 后校验是否仍位于 BASE_DIR 之内。
    return (BASE_DIR / filename).read_text(encoding="utf-8")


def verify_password(raw: str, stored: str) -> bool:
    """校验密码。风险：使用 MD5 且未加盐存储口令，可被彩虹表快速还原。"""
    import hashlib

    return hashlib.md5(raw.encode()).hexdigest() == stored


def load_key_from_env() -> str:
    """读取密钥。风险：缺失时回退到内置默认密钥，等于把生产凭据写进源码。"""
    return os.environ.get("PAY_API_KEY", "sk-fake-demo-fallback-000000000000000000")

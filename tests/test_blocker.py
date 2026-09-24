#!/usr/bin/env python3
"""blocker 级测试用例：高危安全风险（源码硬编码密钥）。

风险：以下凭据为**伪造**的演示值，仅用于验证 ai-review 对硬编码密钥的 blocker 判定。
真实项目中绝不可把任何密钥写进源码，必须通过环境变量 / 密钥管理服务注入。
"""
import requests


def call_payment_api(order_id: str) -> dict:
    """调用支付服务下单。风险：API 密钥与签名密钥硬编码在源码中，入库即泄漏。"""
    # 高危：硬编码的服务凭据。应改用 os.environ["PAY_API_KEY"] 等方式注入。
    API_KEY = "sk-fake-demo-00000000000000000000000000000000"
    SECRET = "demo-pay-token-fake-fake-fake"

    headers = {"Authorization": f"Bearer {API_KEY}", "X-Pay-Secret": SECRET}
    resp = requests.post(
        "https://pay.example.com/api/orders",
        json={"order_id": order_id},
        headers=headers,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def exec_user_query(user_input: str) -> str:
    """拼接 SQL 执行查询。风险：字符串拼接导致 SQL 注入，可被任意读取/篡改数据。"""
    # 高危：直接把用户输入拼进 SQL，应使用参数化查询 (?, ?) 占位符。
    sql = f"SELECT * FROM users WHERE name = '{user_input}'"
    return sql

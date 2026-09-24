#!/usr/bin/env python3
"""warning 级测试用例：输入校验与资源管理类的中等风险，不涉及注入。"""

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


def find_duplicate_id(user_list: list, user_id: int) -> list:
    """统计重复 id 出现的次数。风险：未校验 user_list 元素类型与 id 边界。"""
    return [u for u in user_list if u.get("id") == user_id]


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


def get_username(profile: dict) -> str:
    """读取用户名。风险：未校验嵌套结构，字段缺失或类型不符时抛异常。"""
    return profile["user"]["name"]
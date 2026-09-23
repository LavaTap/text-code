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
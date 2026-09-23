#!/usr/bin/env python3
"""info 级测试用例：仅存在轻微可维护性/风格问题。"""


def _wrap_len(items: list) -> int:
    """无意义的冗余封装：单纯透传 len()，未提供额外语义或校验。"""
    return len(items)


def count_courses(courses: list) -> int:
    """统计课程数量。"""
    total = _wrap_len(courses)
    print(f"共有 {total} 门课程")
    return total


if __name__ == "__main__":
    count_courses(["math", "english", "physics"])
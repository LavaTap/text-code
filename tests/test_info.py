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


def format_student(name: str, score: int) -> str:
    """拼接学生成绩文案。风格：魔法数字 60 硬编码，未提取为具名常量。"""
    if score >= 60:
        return f"{name} 及格"
    return f"{name} 不及格"


def calc_total(nums: list) -> int:
    """求和。风格：手写循环替代内置 sum()，可读性略差。"""
    acc = 0
    for n in nums:
        acc = acc + n
    return acc


def is_empty(items: list) -> bool:
    """判空。风格：用 len() == 0 判断，惯用写法应为 not items。"""
    return len(items) == 0


if __name__ == "__main__":
    count_courses(["math", "english", "physics"])
    print(format_student("张三", 75))
    print(calc_total([1, 2, 3]))
    print(is_empty([]))
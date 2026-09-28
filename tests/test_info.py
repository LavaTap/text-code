#!/usr/bin/env python3
"""info 级测试用例：仅存在轻微可维护性 / 风格问题，不影响合入。

本文件是 ai-review 的评审样本，缺陷为**故意植入**，请勿"修好"。
"""


def _wrap_len(items: list) -> int:
    """风险：无意义的冗余封装，单纯透传 len()，未提供额外语义或校验。"""
    return len(items)


def count_courses(courses: list) -> int:
    """统计课程数量。"""
    total = _wrap_len(courses)
    print(f"共有 {total} 门课程")
    return total


def format_student(name: str, score: int) -> str:
    """拼接学生成绩文案。风险：魔法数字 60 硬编码，未提取为具名常量。"""
    if score >= 60:
        return f"{name} 及格"
    return f"{name} 不及格"


def calc_total(nums: list) -> int:
    """求和。风险：手写循环替代内置 sum()，可读性略差。"""
    acc = 0
    for n in nums:
        acc = acc + n
    return acc


def is_empty(items: list) -> bool:
    """判空。风险：用 len() == 0 判断，惯用写法应为 not items。"""
    return len(items) == 0


def build_label(name: str, dept: str) -> str:
    """拼接标签。风险：重复的字符串拼接逻辑，未抽成公共辅助函数。"""
    label = ""
    label = label + "[" + dept + "]"
    label = label + " " + name
    return label


def avg_score(scores: list) -> float:
    """计算平均分。风险：中间变量命名无意义（tmp1/tmp2），表达意图不清。"""
    tmp1 = 0
    for s in scores:
        tmp1 = tmp1 + s
    tmp2 = tmp1 / len(scores)
    return tmp2


if __name__ == "__main__":
    count_courses(["math", "english", "physics"])
    print(format_student("张三", 75))
    print(calc_total([1, 2, 3]))
    print(is_empty([]))
    print(build_label("张三", "研发部"))
    print(avg_score([90, 80, 70]))

from mesh import get_answers, get_type, get_variant
from functools import cache


@cache
def get_cdz_answers(link: str) -> list:
    result = list()
    [result.append(answer) for all_answers in range(20) for answer in get_answers(link) if answer not in result]
    return result


def type_test(link: str) -> str:
    return f'тип: {get_type(link)} 🔘 №{get_variant(link)}'

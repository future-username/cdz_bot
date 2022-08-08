from src.core.mesh.mesh import *
from functools import cache
# from pandas import Series


@cache
def get_cdz_answers(link: str) -> list:
    # result = list()
    # set(result.append(answer) for _ in range(len(get_answers(link)) + 8)
    #     for answer in get_answers(link) if answer not in result)
    # return result
    # return list(
    #     map(list, {tuple(answer) for _ in range(len(get_answers(link)) + 5) for answer in get_answers(link)}))
    # new = [answer for _ in range(len(get_answers(link)) + 8) for answer in get_answers(link)]
    # return Series(new).drop_duplicates().tolist()
    return list(map(list, {tuple(answer) for _ in range(len(get_answers(link)) + 5) for answer in get_answers(link)}))


def type_test(link: str) -> str:
    return f'тип: {get_type(link)} 🔘 №{get_variant(link)}'

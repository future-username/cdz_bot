from mesh import get_answers, get_type, get_variant
from functools import cache


@cache
def get_cdz_answers(link: str):
    try:
        result_answers = []
        for all_answers in range(len(get_answers(link))):
            answers = get_answers(link)
            [result_answers.append(answer) for answer in answers if answer not in result_answers]
        return result_answers
    except:
        return '⚠️Хм странно, но я ничего не нашел. Проверь правильность ссылки или нажми 👉/help👈'

    
def type_test(link: str):
    return f'тип: {get_type(link)}, №{get_variant(link)}'

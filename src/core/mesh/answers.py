from src.core.mesh.utils import *


def answer_single(answer_data: dict) -> str:
    answer_id = answer_data["right_answer"]["id"]
    return ''.join([generate_string(entry) for entry in answer_data["options"] if entry["id"] == answer_id])


def answer_string(answer_data: dict) -> str: return generate_string(answer_data["right_answer"])


def answer_order(answer_data: dict, answer='') -> str:
    order_ids = answer_data["right_answer"]["ids_order"]
    answer += ''.join([f"{generate_string(answer_entry)} 🔘 " for correct_order_element in order_ids
                       for answer_entry in answer_data["options"] if answer_entry["id"] == correct_order_element])
    return answer[:-2]


def answer_groups(answer_data: dict, answer='', group_name='', group_elements='') -> str:
    correct_groups = answer_data["right_answer"]["groups"]

    for group in correct_groups:
        for answer_entry in answer_data["options"]:
            if answer_entry["id"] in group["options_ids"]:
                group_elements += f"{generate_string(answer_entry)} 🔘 \n\t"
            elif answer_entry["id"] == group["group_id"]:
                group_name = generate_string(answer_entry)

        answer += f"{group_name}:\n\t{group_elements}"

    return answer[:-2]


def answer_table(answer_data: dict, answer='') -> str:
    answer_dict = {}

    cell_names = answer_data["options"][0]["content"][0]["table"]["cells"]
    answer_cells = answer_data["right_answer"]["cells"]

    for index in cell_names.keys():
        answer_dict[index] = cell_names[index] | answer_cells[index]\
            if index in answer_cells.keys() else cell_names[index]

    answer += ''.join([f"{' 🔘 '.join(row.values())}\n\t" for row in answer_dict.values()])
    return answer


def answer_multiple(answer_data: dict, answer='') -> str:
    answer_ids = answer_data["right_answer"]["ids"]
    answer += ''.join([f"{generate_string(answer_entry)} 🔘 " for answer_id in answer_ids
                       for answer_entry in answer_data["options"] if answer_entry["id"] == answer_id])
    return answer[:-2]


def answer_inline_choice_single(answer_data: dict, answer='') -> str:
    answer_ids = answer_data["right_answer"]["text_position_answer"]

    for field_num, answer_id in enumerate(answer_ids):
        entry_options = answer_data["text_position"][field_num]["options"]
        answer += ''.join([f"{generate_string(entry)} 🔘 " for entry in entry_options if entry["id"] == answer_id["id"]])
    return answer[:-2]


def answer_number(answer_data: dict) -> str: return str(answer_data["right_answer"]["number"])


def answer_match(answer_data: dict, answer='', key_name='', value_name='') -> str:
    correct_elements = answer_data["right_answer"]["match"]

    for key, value in correct_elements.items():
        for answer_entry in answer_data["options"]:
            if answer_entry["id"] == key:
                key_name = generate_string(answer_entry)
            elif answer_entry["id"] == value[0]:
                value_name = generate_string(answer_entry)

        answer += f" \n{key_name}: {value_name}"
    return answer


def answer_gap_match_text(answer_data: dict, answer='') -> str:
    answer_ids = answer_data["right_answer"]["text_position_answer"]
    answer += ''.join([f"{generate_string(answer_option)} 🔘 " for answer_id in answer_ids
                       for answer_option in answer_data["options"] if answer_id["id"] == answer_option["id"]])
    return answer[:-2]

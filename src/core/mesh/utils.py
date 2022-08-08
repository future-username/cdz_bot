from re import compile


def convert_latex(string: str) -> str:
    string = string.replace("\\", "")

    simple_transforms = {
        "\\^circ": ["^circ", " градусов"],
        "bigtriangleup": ["bigtriangleup", "треугольник"],
        "angle": ["angle", "/_"],
        "cdot": ["cdot", "*"],
        "ge": ["ge", ">="],
        "le": ["le", "<="],
        "infty": ["infty", "∞"],
    }

    for regex, changes in simple_transforms.items():
        index = compile(regex)
        for _ in index.findall(string):
            string = string.replace(changes[0], changes[1])

    fraction = compile("frac{(.*?)}{(.*?)}")
    square_root = compile("sqrt{(.*?)}")
    power = compile("(.*?)\\^(.*)")

    for i in fraction.findall(string):
        string = string.replace("frac{" + str(i[0]) + "}{" + str(i[1]) + "}", f'({str(i[0])}) / ({str(i[1])})')

    for i in square_root.findall(string):
        string = string.replace("sqrt{" + str(i) + "}", f" корень из ({str(i)})")

    for i in power.findall(string):
        string = string.replace(f"{str(i[0])}^{str(i[1])}", f"{str(i[0])} в степени ({str(i[1])})")

    string = string.replace('^', ' в степени ')
    return string


def remove_soft_hypen(sentence: str) -> str:
    sentence = sentence.replace('\xad', '')
    sentence = sentence.replace('\u00ad', '')
    sentence = sentence.replace('\N{SOFT HYPHEN}', '')

    return sentence


def generate_string(string_data: dict, move_point=0) -> str:
    parameters = string_data.keys()

    if "text" in parameters:
        text = string_data["text"]

        for option in string_data["content"]:
            option_text = convert_latex(option["content"]) if option["type"] == "content/math" else option["content"]
            insert_index = option["position"] + move_point
            text = f"{text[:insert_index]} {option_text} {text[insert_index:]}"
            move_point += 2 + len(option_text)

        return text

    elif "string" in parameters:
        return convert_latex(string_data["string"])

    elif "atomic_id" in parameters:
        atomic_type = string_data["atomic_type"]

        if atomic_type == "image":
            return f" (https://uchebnik.mos.ru/cms{string_data['preview_url']}) "
        elif atomic_type == "sound":
            return f" ({string_data['preview_url']}) "

        elif atomic_type == "video":
            return f" ({string_data['preview_url']}) "

    elif "file" in parameters:
        file_location = string_data["file"]["relative_url"]
        return f" (https://uchebnik.mos.ru/webtests/exam{file_location}) "

    else:
        return ""

import re

def normalise_name(name):
    if not isinstance(name, str) or name == "":
        raise ValueError("Filename must be a non-empty string")

    name_no_spaces = re.sub(r"\s+", "", name)
    name_no_unwanted_chars = re.sub(r"[.''%]", "", name_no_spaces)
    name_with_underscores = re.sub(r"(?<!^)(?=[A-Z])", "_", name_no_unwanted_chars)
    collapsed_underscores = re.sub(r"_+", "_", name_with_underscores)
    name_without_numbers = re.sub(r"\d+", "", collapsed_underscores)
    ascii_only = re.sub(r"[^a-zA-Z0-9_]", "", name_without_numbers)
    clean_name = ascii_only.strip("_")
    return clean_name
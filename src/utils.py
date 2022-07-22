def sanitize_string_for_csv(input_string: str):
    return input_string.replace(',', '').replace(';', '')


def sanitize_string_for_database(input_string: str):
    return input_string.replace('\'', '')


def unify_item_name(input_string: str):
    """
    Takes input string and converts it to lowercase, no special characters, no spaces string
    :param input_string:
    :return:
    """
    chars = '-\\/_\''
    for c in chars:
        input_string = input_string.replace(c, '')

    return input_string.replace(' ', '').lower()

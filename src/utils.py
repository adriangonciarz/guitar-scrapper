def sanitize_string_for_csv(input_string: str):
    return input_string.replace(',', '').replace(';', '')


def sanitize_string_for_database(input_string: str):
    return input_string.replace('\'', '\'\'')


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


def check_if_result_matches_substring(result: str, substring: str):
    def chunkify(text: str):
        return text.replace('\'', '').replace('-', ' ').replace('\\', '').replace('/', ' ').lower().split()

    result_split = chunkify(result)
    substring_split = chunkify(substring)
    return all(map(lambda word: word in result_split, substring_split))

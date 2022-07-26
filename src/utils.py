def sanitize_string_for_csv(input_string: str):
    return input_string.replace(',', '').replace(';', '')


def sanitize_string_for_database(input_string: str):
    return input_string.replace('\'', '\'\'')


def check_if_result_matches_substring(result: str, substring: str):
    def chunkify(text: str):
        return text.replace('\'', '').replace('-', ' ').replace('\\', '').replace('/', ' ').lower().split()

    result_split = chunkify(result)
    substring_split = chunkify(substring)
    return all(map(lambda word: word in result_split, substring_split))

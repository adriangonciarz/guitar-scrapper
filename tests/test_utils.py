import pytest

from utils import sanitize_string_for_csv, sanitize_string_for_database, check_if_result_matches_substring


def test_sanitzing_string_for_csv():
    test_string = 'Super awesome; buy, now!'
    assert sanitize_string_for_csv(test_string) == 'Super awesome buy now!'


def test_sanitizing_string_for_database():
    test_string = "Paul's guitar"
    assert sanitize_string_for_database(test_string) == "Paul''s guitar"


@pytest.mark.parametrize(
    "result,model,matched", [
        ("Fender Custom Shop '62 Reissue Stratocaster Journe", 'Stratocaster Custom Shop', True),
        ("Fender Custom Shop '62 Reissue Stratocaster Journe", 'Telecaster Custom Shop', False),
        ("Eastman SB59 /V + HardCase beter dan Gibson Les Paul custom", 'SB59', True),
        ("Eastman sb 59 type les paul", 'SB-59', True),
        ("PRS Paul's Guitar", "Paul's Guitar", True),
        ("PRS Pauls Guitar", "Paul's Guitar", True),
        ("PRS Custom 24", 'Custom 24', True),
        ("PRS Custom-24", 'Custom 24', True),
        ("PRS Custom-24", 'Custom 22', False),
        ("PRS CU 24", 'CU-24', True),
        ("PRS CU 24", 'CU-22', False),
        ("PRS CU 24", 'PRS', True),
        ("Music Man Axis Floyd Rose", 'Music Man', True),
    ]
)
def test_checking_result_matching(result, model, matched):
    assert check_if_result_matches_substring(result, model) == matched

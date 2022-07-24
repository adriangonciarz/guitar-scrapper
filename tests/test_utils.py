import pytest

from utils import sanitize_string_for_csv, unify_item_name, sanitize_string_for_database, check_if_result_matches_model


def test_sanitzing_string_for_csv():
    test_string = 'Super awesome; buy, now!'
    assert sanitize_string_for_csv(test_string) == 'Super awesome buy now!'


def test_sanitizing_string_for_database():
    test_string = "Paul's guitar"
    assert sanitize_string_for_database(test_string) == "Paul''s guitar"


def test_cleanup_name():
    test_name = 'Eastman SB-57/V'
    assert unify_item_name(test_name) == 'eastmansb57v'

@pytest.mark.parametrize(
    "result,model,matched", [
        ("Fender Custom Shop '62 Reissue Stratocaster Journe", 'Stratocaster Custom Shop', True),
        ("Fender Custom Shop '62 Reissue Stratocaster Journe", 'Telecaster Custom Shop', False),
        ("Eastman SB59 /V + HardCase beter dan Gibson Les Paul custom", 'SB-59', True),
        ("Eastman sb 59 type les paul", 'SB-59', True),
    ]
)
def test_checking_if_result_matching(result, model, matched):
    assert check_if_result_matches_model(result, model) == matched

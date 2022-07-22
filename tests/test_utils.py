from utils import sanitize_string_for_csv, unify_item_name


def test_sanitzing_string_for_csv():
    test_string = 'Super awesome; buy, now!'
    assert sanitize_string_for_csv(test_string) == 'Super awesome buy now!'


def test_cleanup_name():
    test_name = 'Eastman SB-57/V'
    assert unify_item_name(test_name) == 'eastmansb57v'

import os

from assertpy import assert_that

from models import SearchManager

test_config_filepath = os.path.join(os.getcwd(), 'test_brand_config.yaml')


def test_loading_config():
    sm = SearchManager(test_config_filepath)
    assert len(sm.brands) == 3


def test_get_brands():
    expected_brands = ['Music Man', 'Eastman', 'Kelton']
    sm = SearchManager(test_config_filepath)
    assert_that(sm.get_brands()).is_equal_to(expected_brands)


def test_get_search_terms():
    expected_search_terms = [
        'music man luke',
        'eastman sb57',
        'kelton swade'
    ]
    sm = SearchManager(test_config_filepath)
    assert_that(sm.get_search_terms()).is_equal_to(expected_search_terms)

import os

import pytest
from assertpy import assert_that

from config.config import BrandManager

test_config_filepath = os.path.join(os.getcwd(), 'test_brand_config.yaml')


def test_loading_config():
    bm = BrandManager(test_config_filepath)
    assert len(bm.brands) == 3


def test_get_brands():
    expected_brands = ['Music Man', 'Eastman', 'Kelton Swade']
    bm = BrandManager(test_config_filepath)
    assert_that(bm.get_brand_names()).is_equal_to(expected_brands)


def test_get_search_terms():
    expected_search_terms = [
        'music man luke',
        'eastman sb57',
        'kelton swade avrt'
    ]
    bm = BrandManager(test_config_filepath)
    assert_that(bm.get_search_terms()).is_equal_to(expected_search_terms)


@pytest.mark.parametrize(
    'search_string,brand_name', [
        ('Amazing, mint condition Music Man Luke II orange!', 'Music Man'),
        ('Unique kelton swade telecaster AVRT', 'Kelton Swade'),
        ('Amazing, mint condition musicman Luke II orange!', 'Music Man'),
        ('Amazing, mint condition EBMM Luke 3 HSS orange!', 'Music Man'),
    ]
)
def test_successful_brand_matching(search_string, brand_name):
    bm = BrandManager(test_config_filepath)
    assert bm.find_matching_brand(search_string) == brand_name


@pytest.mark.parametrize(
    'search_string,model_name', [
        ('Amazing, mint condition Music Man Luke II orange!', 'Luke'),
        ('Unique kelton swade telecaster AVRT', 'AVRT'),
        ('Amazing, mint condition musicman Lukather II orange!', 'Luke'),
        ('Like-new Eastman Sb-57/V flamed maple', 'SB57'),
    ]
)
def test_successful_model_matching(search_string, model_name):
    bm = BrandManager(test_config_filepath)
    brand_name = bm.find_matching_brand(search_string)
    assert bm.find_matching_model(brand_name, search_string) == model_name

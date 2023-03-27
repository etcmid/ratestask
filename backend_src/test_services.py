from datetime import datetime
from decimal import Decimal
import os

from api.services import ApiService


# define the test input data
test_date_from = '2016-01-01'
test_date_to = '2016-01-10'
test_date_from = datetime.strptime(test_date_from, "%Y-%m-%d").date()
test_date_to = datetime.strptime(test_date_to, "%Y-%m-%d").date()
test_origin = 'CNSGH'
test_destination = 'north_europe_main'
test_db_url = os.environ['DATABASE_URL']

expected = [{'day': '2016-01-01', 'round': Decimal('1077')},
            {'day': '2016-01-02', 'round': Decimal('1077')},
            {'day': '2016-01-03', 'round': None},
            {'day': '2016-01-04', 'round': None},
            {'day': '2016-01-05', 'round': Decimal('1116')},
            {'day': '2016-01-06', 'round': Decimal('1117')},
            {'day': '2016-01-07', 'round': Decimal('1110')},
            {'day': '2016-01-08', 'round': Decimal('1094')},
            {'day': '2016-01-09', 'round': Decimal('1094')},
            {'day': '2016-01-10', 'round': Decimal('1094')}]



def test_get_prices_len():

    # create an instance of ApiService with the test database URL
    api_service = ApiService(test_db_url)

    # call the get_prices() method with the test input data
    prices = api_service.get_prices(
        test_date_from, test_date_to, test_origin, test_destination)

    assert len(prices) == 10


def test_get_prices_data():

    # create an instance of ApiService with the test database URL
    api_service = ApiService(test_db_url)

    # call the get_prices() method with the test input data
    prices = api_service.get_prices(
        test_date_from, test_date_to, test_origin, test_destination)

    assert prices == expected

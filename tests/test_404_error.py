# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import pytest
from pytest_mock import mocker
import airqualityindex as aqi
import requests

def test_404(requests_mock, mocker):
    fake_url = 'http://123-fake-api.com'

    requests_mock.get(fake_url + '/feed/city/?token=token',
            status_code='404',
            text='Not Found')

    mocker.spy(aqi.RestApiRequestMaker, '_behaviour_in_case_of_404_error')
    waqi = aqi.RestApiRequestMaker( fake_url, 'token')

    waqi.print_city_feed('city')

    assert waqi.latest_error_code == '404'
    assert waqi._behaviour_in_case_of_404_error.call_count == 1








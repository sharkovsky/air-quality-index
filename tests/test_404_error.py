import airqualityindex as aqi
import requests
from requests.exceptions import HTTPError


def test_404(requests_mock, mocker):

    requests_mock.get('http://api.waqi.info/feed/city/?token=token',
                      status_code=requests.codes.not_found,
                      text='Not Found')

    mocker.spy(aqi.WAQI, '_behaviour_in_case_of_404_error')
    waqi = aqi.WAQI('token')

    try:
        _ = waqi.get_air_quality('city')
    except HTTPError as e:
        assert e.response.status_code == requests.codes.not_found

    assert waqi._behaviour_in_case_of_404_error.call_count == 1

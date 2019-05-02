import airqualityindex as aqi


def test_404(requests_mock, mocker):
    fake_url = 'http://123-fake-api.com'

    requests_mock.get(fake_url + '/feed/city/?token=token',
                      status_code='404',
                      text='Not Found')

    mocker.spy(aqi.RestApiRequestMaker, '_behaviour_in_case_of_404_error')
    waqi = aqi.RestApiRequestMaker(fake_url, 'token')

    waqi.print_city_feed('city')

    assert waqi.latest_error_code == '404'
    assert waqi._behaviour_in_case_of_404_error.call_count == 1

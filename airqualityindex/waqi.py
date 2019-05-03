import requests


__all__ = ['WAQI']


class WAQI:
    def __init__(self, token_):
        self.token = token_
        self._session = requests.Session()
        self._session.params = {'token': self.token}

    @property
    def _domain_url(self):
        return 'http://api.waqi.info'

    def _request_city_feed(self, city_name):
        request_url = self._domain_url + '/feed/' + city_name + '/'
        res = self._session.get(request_url)
        return res

    def _behaviour_in_case_of_404_error(self, response):
        # do other things before
        response.raise_for_status()

    def get_air_quality(self, city_name):
        res = self._request_city_feed(city_name)

        if res.status_code == requests.codes.not_found:
            self._behaviour_in_case_of_404_error(res)
        else:
            res.raise_for_status()

        data = res.json()
        aqi = data['data']['aqi']
        nicer_city_name = data['data']['city']['name']
        return dict(
            city=nicer_city_name,
            aqi=aqi
        )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', '-c',
                        required=True,
                        default='hongkong',
                        help='city to query [default: hongkong]')
    args = parser.parse_args()

    with open('data/waqi_token.txt') as f:
        token = f.readlines()[0].strip()

    waqi = WAQI(token)

    airquality = waqi.get_air_quality(args.city)

    print('Air Quality Index in', airquality['city'], 'is', airquality['aqi'])

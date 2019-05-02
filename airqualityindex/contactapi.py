import requests

class RestApiRequestMaker():
    def __init__(self, base_url_, token_):
        self.base_url = base_url_
        self.token = token_
        self.latest_error_code = None

    def _request_city_feed(self, city_name):
        request_url = self.base_url + '/feed/' + city_name + '/?token=' + self.token 
        res = requests.get( request_url )
        return res

    def _behaviour_in_case_of_404_error(self, status_code):
        self.latest_error_code = status_code

    def print_city_feed(self, city_name):
        res = self._request_city_feed(city_name)
        if res.status_code == '404':
            self._behaviour_in_case_of_404_error(res.status_code)
        else:
            data = res.json()
            aqi = data['data']['aqi']
            nicer_city_name = data['data']['city']['name']
            print( 'Air Quality Index in', nicer_city_name, 'is', aqi)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', '-c', required=True,
            type=str, help='city to query')
    args = parser.parse_args()

    with open('data/waqi_token.txt', 'r') as f:
        token = f.readlines()[0].strip()

    WAQI = RestApiRequestMaker(
            'http://api.waqi.info',
            token,
            )

    WAQI.print_city_feed(args.city)

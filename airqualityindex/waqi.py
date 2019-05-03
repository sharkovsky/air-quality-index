# -*- coding: utf-8 -*-
"""World Air Quality Index (WAQI).

This module implements the necessary logic to retrieve the Air Quality Index of a
given city, by contacting the WAQI REST API.
It also tries to handle 404 errors.

Example:
    To obtain information for Hong Kong:

    $ python -m airqualityindex.waqi --city hongkong
"""


import requests


__all__ = ['WAQI']


class WAQI:
    """Air Quality Index from waqi REST API.

    This class can obtain the Air Quality Index by making
    requests to the waqi API.

    Attributes:
        token: a string containing the API token
    """

    def __init__(self, token_):
        """Inits WAQI with an API token.

        Args:
            token_: a string containing the API token
        """
        self.token = token_
        self._session = requests.Session()
        self._session.params = {'token': self.token}

    @property
    def _domain_url(self):
        return 'http://api.waqi.info'

    def _request_city_feed(self, city_name):
        """Performs the API request."""
        request_url = self._domain_url + '/feed/' + city_name + '/'
        res = self._session.get(request_url)
        return res

    def _behaviour_in_case_of_404_error(self, response):
        """Implements requested behaviour in case of 404.

        This is a dummy function to help showcase
        mocking in tests.
        """
        response.raise_for_status()

    def get_air_quality(self, city_name):
        """Get air quality index from API.

        Peforms a request to the API, tries to handle 404 errors
        and packages the results in a dictionary.

        Args:
            city_name: a string with the name of the city to be
                queried. This name *must* be in the format
                that the waqi API accepts.

        Returns:
            A dict with keys
                city: a string with a nicely formatted name of
                    the queried city, as returned by the waqi API.
                aqi: a float value of the air quality index.
        """

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

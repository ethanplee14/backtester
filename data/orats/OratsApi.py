import requests


class OratsApi:

    BASE_URL = "https://api.orats.io/datav2/"

    def __init__(self, token):
        self.token = token

    def fetch(self, endpoint, **kwargs):
        """
        Fetches market_data from orats rest api
        :param endpoint: API endpoint formatted as "path/to/endpoint"
        :param kwargs: Arguments for querystring of endpoint
        :return: api get response
        """
        url = self.BASE_URL + endpoint
        response = requests.get(url, {
            "token": self.token,
            **kwargs
        })
        if response.status_code != 200:
            raise requests.HTTPError(response.text)
        return response.json()['market_data']

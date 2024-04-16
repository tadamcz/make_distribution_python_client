import requests


class APIClient:
    def __init__(self, token):
        self.base_url = "http://makedistribution.com/s/api/v0"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {token}"})

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return self.session.request(method, url, **kwargs)

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

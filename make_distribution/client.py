import requests


class JSONClient:
    def __init__(self, token, version="v0"):
        self.base_url = f"https://makedistribution.com/s/api/{version}"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {token}"})

    def _request(self, method, endpoint, **kwargs) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            # Attempt to raise a more informative error message
            try:
                body = response.json()
                message = f"HTTP {response.status_code}: {body}"
            except ValueError:
                message = None
            if message:
                # Raise a new exception with the informative message
                raise requests.HTTPError(message, response=response)
            else:
                # Re-raise the original exception
                raise
        return response.json()

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

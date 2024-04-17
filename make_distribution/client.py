import re
from typing import Union, List

import requests

from make_distribution.distributions import Distribution


class JSONClient:
    def __init__(self, token=None, version="v0"):
        self.base_url = f"https://makedistribution.com/s/api/{version}"
        self.session = requests.Session()
        if token:
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


class SciPyClient:
    """
    Instead of basic data structures, this client returns objects that follow the interface
    of SciPy's distributions (specifically, the 'frozen' instances inheriting from
    ``rv_continuous_frozen``).
    """

    def __init__(self, client: JSONClient):
        self.client = client

    ALLOWED_ENDPOINTS = [
        {"methods": ["POST", "GET"], "endpoint": "1d/dists/", "id_pattern": r"[\w-]+"},
        {
            "methods": ["GET", "PUT", "PATCH", "DELETE"],
            "endpoint": "1d/dists/{id}/",
            "id_pattern": r"[\w-]+",
        },
        {"methods": ["POST", "GET"], "endpoint": "1d/mixtures/", "id_pattern": r"[\w-]+"},
        {
            "methods": ["GET", "PUT", "PATCH", "DELETE"],
            "endpoint": "1d/mixtures/{id}/",
            "id_pattern": r"[\w-]+",
        },
    ]

    def _request(self, method, endpoint, **kwargs) -> Union[Distribution, List[Distribution]]:
        # Extract the components from the endpoint
        match = re.match(r"(1d/(?:dists|mixtures))(?:/(\w+))?/?", endpoint)

        if not match:
            raise ValueError(f"Invalid endpoint: {endpoint}")

        endpoint_slug, dist_id = match.groups()

        # Check if the method and endpoint are allowed
        # TODO: needs a better error message or fallback behavior if the only problem
        #     is leading/trailing slashes
        for allowed in self.ALLOWED_ENDPOINTS:
            if method in allowed["methods"] and re.match(
                allowed["endpoint"].replace("{id}", allowed["id_pattern"]), endpoint
            ):
                break
        else:
            raise ValueError(
                f"Using SciPyClient, method {method} and endpoint {endpoint} are not allowed"
            )

        if endpoint in ["1d/dists/", "1d/mixtures/"] and method == "GET":
            many = True
        else:
            many = False

        data = self.client._request(method, endpoint, **kwargs)

        if many:
            return [
                Distribution(data=d, endpoint_slug=endpoint_slug, client=self.client) for d in data
            ]
        else:
            return Distribution(data=data, endpoint_slug=endpoint_slug, client=self.client)

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

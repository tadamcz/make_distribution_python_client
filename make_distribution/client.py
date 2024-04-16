import requests


class APIClient:
    def __init__(self, token):
        self.base_url = "http://makedistribution.com/s/api/v0"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {token}"})

    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}/{endpoint}", **kwargs)

    def post(self, endpoint, **kwargs):
        return self.session.post(f"{self.base_url}/{endpoint}", **kwargs)

    def put(self, endpoint, **kwargs):
        return self.session.put(f"{self.base_url}/{endpoint}", **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.session.patch(f"{self.base_url}/{endpoint}", **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}/{endpoint}", **kwargs)

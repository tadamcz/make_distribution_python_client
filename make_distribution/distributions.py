import numpy as np


class Distribution:
    """
    Roughly follows ``rv_continuous_frozen`` interface.
    """

    def __init__(self, data, endpoint_slug, client: "JSONClient"):
        self.data = data
        self.client = client
        self.endpoint_slug = endpoint_slug

    def base_endpoint(self):
        id = self.data["id"]
        return f"{self.endpoint_slug}/{id}/"

    def cdf(self, x):
        endpoint = self.base_endpoint() + "cdf/"
        params = {"x": to_csv_query_param(x)}
        data = self.client.get(endpoint, params=params)
        data = [e["p"] for e in data]
        return np.array(data)

    def pdf(self, x):
        endpoint = self.base_endpoint() + "pdf/"
        params = {"x": to_csv_query_param(x)}
        data = self.client.get(endpoint, params=params)
        data = [e["density"] for e in data]
        return np.array(data)

    def ppf(self, q):
        endpoint = self.base_endpoint() + "qf/"
        params = {"p": to_csv_query_param(q)}
        data = self.client.get(endpoint, params=params)
        data = [e["x"] for e in data]
        return np.array(data)

    def rvs(self, size):
        endpoint = self.base_endpoint() + "samples/"
        params = {"size": size}
        data = self.client.get(endpoint, params=params)
        data = data["samples"]
        return np.array(data)


def to_csv_query_param(o):
    if isinstance(o, list):
        return ",".join([str(x) for x in o])
    return str(o)

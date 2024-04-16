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

    def _arr_request(self, endpoint, in_kwd, in_data, out_kwd):
        """
        Helper for methods that take in arrays as query parameters.
        """
        params = {in_kwd: to_csv_query_param(in_data)}
        data = self.client.get(endpoint, params=params)
        data = [e[out_kwd] for e in data]
        return np.array(data)

    def cdf(self, x):
        endpoint = self.base_endpoint() + "cdf/"
        return self._arr_request(endpoint, in_kwd="x", in_data=x, out_kwd="p")

    def pdf(self, x):
        endpoint = self.base_endpoint() + "pdf/"
        return self._arr_request(endpoint, in_kwd="x", in_data=x, out_kwd="density")

    def ppf(self, q):
        endpoint = self.base_endpoint() + "qf/"
        return self._arr_request(endpoint, in_kwd="p", in_data=q, out_kwd="x")

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

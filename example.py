import os

import make_distribution.client

TOKEN = os.environ["MAKEDISTRIBUTION_API_TOKEN"]

client = make_distribution.client.JSONClient(token=TOKEN)
dist = {
    "family": {"requested": "cinterp5_01"},
    "arguments": {
        "quantiles": [
            {
                "p": 0.1,
                "x": 0,
            },
            {
                "p": 0.5,
                "x": 1,
            },
            {
                "p": 0.9,
                "x": 4,
            },
        ]
    },
}

scipyclient = make_distribution.client.SciPyClient(client)

d = scipyclient.post("1d/dists/", json=dist)
cdf = d.cdf([0, 1, 2])
pdf = d.pdf([0, 1, 2])
ppf = d.ppf([0.1, 0.5, 0.9])
rvs = d.rvs(10)
exit()

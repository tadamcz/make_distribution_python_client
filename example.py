import os

import make_distribution.client

TOKEN = os.environ["MAKEDISTRIBUTION_API_TOKEN"]

client = make_distribution.client.APIClient(token=TOKEN)
dist = {
    "family": {"requested": "cinterp5_01"},
}
r = client.post("1d/dists/", json=dist)

exit()

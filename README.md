
[homepage]: https://makedistribution.com
[docs]: https://makedistribution.com/s/api/v0/docs/

Python client for the [MakeDistribution][homepage] API ([docs][docs]).

Offers a thin wrapper around the API (`JSONClient`) as well as the `Distribution` class which lets you interact with MakeDistribution.com distributions as if they were ordinary SciPy distribution objects. 

At the moment, `Distribution` supports commonly used functionality which should be sufficient for the great majority of use cases. Eventually, the goal is to provide a full drop-in replacement for SciPy's distributions (specifically, ``rv_continuous_frozen``).

# Installation
```bash
pip install make_distribution  # or `poetry add make_distribution`
```

# Usage
```python
import os

import make_distribution.client

TOKEN = os.environ["MAKEDISTRIBUTION_API_TOKEN"]

json_client = make_distribution.client.JSONClient(token=TOKEN)

client = make_distribution.client.SciPyClient(json_client)

data = {
    # See API docs for available families
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

# `dist` is an instance of class `Distribution`
dist = client.post("1d/dists/", json=data)

# Print basic information about the distribution
print(dist)

# `dist` lets you query other endpoints with a SciPy-like interface
size = 5
print(f"rvs(size={size}) = {dist.rvs(size)}")  # Draw random samples

x = [1, 2, 3]
print(f"cdf({x}) = {dist.cdf(x)}") # Cumulative distribution function
print(f"pdf({x}) = {dist.pdf(x)}") # Probability density function

p = [0.1, 0.2, 0.3]
print(f"ppf({p}) = {dist.ppf(p)}") # Quantile function (inverse CDF)
```
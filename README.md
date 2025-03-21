# Metaflow QA test suite

## Install requirements

```sh
pip install -r requirements.txt
```

## Setup

Make sure you have a working Metaflow installation that can be used to execute the flows in the test cases. This includes deploying and running flows on Argo Workflows.

## Run the test suite

use `pytest` to gather and run the individual tests. The following command will run many test cases in parallel with `pytest-xdist`

```sh
pytest -n auto
```

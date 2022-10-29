# Developer's Note

## Tests

The unittests for this library is written using [`pytest`](https://docs.pytest.org/). The configs for the tests module can be found in the root of the project as `pytest.ini`.

Now most of the tests for this project can be performed without any hiccup, but when it comes to testing with the MongoDB conection, we'd have to rely on Docker
or the CICD pipelines. So by default the script that tests `monolg` in presence of the MongoDB database, will stay excluded. So,

**To run the tests (excluding MongoDB available scenario) do the following**

```bash
pytest tests -v --cov
```

**If we explicitly want to run the script that tests the Monolg class at its fullest extend, do the following**

```bash
pytest tests/test_monolg.py -v --cov
```

**NOTE**: The script test_monolg.py is written for scenarios where MongoDB is available.

__Markers__

Following the different [pytest markers](https://docs.pytest.org/en/7.1.x/example/markers.html) used in this test suite.

|Marker|Description|Test script|
|:-----|:----------|:----------|
|`schema`|Project's schema related unittests|`tests/test_schemas.py`|
|`configs`|Tests for the configuration file & the keys|`tests/test_configs.py`|
|`utils`|Tests for the utility metthods|`tests/test_utils.py`|
|`monolg`|Tests for the class `Monolg`|`tests/test_monolg_wo_conn.py`|

**To test any using particular marker do the following, for example take `configs`**

```bash
pytest -v -m configs
```

## Documentation

The documentation for this project uses ``mkdocs``

Serving the docs locally
```bash
mkdocs serve
```

Building the docs locally
```bash
mkdocs build
```

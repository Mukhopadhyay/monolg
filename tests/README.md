# Tests for `monolg`

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

## Test cases for `monolg`

### Establishing connection

* Try connecting `monolg` when MongoDB is not running (using default params)
**Expected result:** Appropriate exception should be thrown

* Try connecting `monolg` when MongoDB is running (using default params)
**Expected result:** The instance should be able to make a connection & if the `sys_log` flag is enabled then the connection established log should be in the system log collection.

* Try connecting `monolg` using a connection string when MongoDB is not running.


* Try connecting `monolg` using a connection string when MongoDB is running.

- [ ] Try connecting to Mongo (While Mongo is running)
- [ ] `.connect` while mongo is not running.
- [ ] Try logging before connecting
- [ ] Check default verbose settings (Should be `True`)
- [ ] Check if default data value is `None` and not `{}`
- [ ] Connect & check in the system logs if we find the right DB & collection name
- [ ] After closing the connecting and reopening it, we should have 2 entries in system logs with the same datetime (one with connection message and one with reopen message)
- [ ] Check the flags before & after connecting
- [ ] After closing collection even sys logs shouldn't go through

<!-- |**ID**|**Scenario**|**Precondition**|**Expected result**|Implemented|
|:-----|:-----------|:---------------|:------------------|:----------|
|1|Try connecting to `monolg` with default params|MongoDB is not running|Appropriate error message should be displayed||
|2|Try connecting to `monolg` with default params|MongoDB is running|Connection should be established||
|3|Try and connect to `monolg` using a connection string|MongoDB is not running|Appropriate error message should be displayed||
|4|Try and connect to `monolg` using a connection string|MongoDB is running|Connection should be established|| -->


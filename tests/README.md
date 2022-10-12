Tests for `monolg`

## Running the tests

```bash
pytest tests -v --cov
```

__Markers__

|Marker|Description|Test script|
|:-----|:----------|:----------------------|
|`schema`|Project's schema related unittests|`tests/test_schemas.py`|
|`configs`|Tests for the configuration file & the keys|`tests/test_configs.py`|
|`utils`|Tests for the utility metthods|`tests/test_utils.py`|
|`monolg`|Tests for the class `Monolg`|`tests/test_monolg.py`|


## Test cases

- [ ] Try connecting to Mongo (While Mongo is running)
- [ ] `.connect` while mongo is not running.
- [ ] Try logging before connecting
- [ ] Check default verbose settings (Should be `True`)
- [ ] Check if default data value is `None` and not `{}`
- [ ] Connect & check in the system logs if we find the right DB & collection name
- [ ] After closing the connecting and reopening it, we should have 2 entries in system logs with the same datetime (one with connection message and one with reopen message)
- [ ] Check the flags before & after connecting
- [ ] After closing collection even sys logs shouldn't go through


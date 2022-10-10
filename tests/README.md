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

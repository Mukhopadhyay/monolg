# Getting started with `monolg`

Before you start, just know that the main motivation behind this library was to keep the interface as pythonic as possible. So you'll find alot of familiarity with the default `logging` library. We even have the same set of logging functions that we can perform in the logging library.

Let us get started with...

## Installation

Monolg can be installed from PyPI using the following:

```bash
$ pip install monolg
```

or you can install directly from github using.
```bash
$ pip install git+https://github.com/Mukhopadhyay/monolg.git
```

Comparing code with the `logging` module

If you want to get started with logging using the built-in `logging` API provided by the standard library modules you would have to do the following

```python
import logging

# Setting up the logger
logging.basicConfig(filename='test.log', level=logging.INFO)
logging.info('Hello, World!')

>>> INFO:root:Hello, World!
```

Whereas, if we compare that to `Monolg` that is more if not as simpler,

```python
from monolg import Monolg

mlog = Monolg('mongodb://localhost:27017', verbose=True)
mlog.conect()  # Connecting to the MongoDB instance
mlog.info("Welcome to monolg")

>>> 10-10-2022 10:10:10 [INFO] [system] monolg connected to mongodb
>>> 10-10-2022 10:10:10 [INFO] [monolg] Welcome to monolg
```

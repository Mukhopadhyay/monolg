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

Basic usage

```python
from monolg import Monolg

mlog = Monolg()
mlog.info("Welcome to monolg")
```

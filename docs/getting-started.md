# Getting started

Before you start, just know that the main motivation behind this library was to keep the interface as pythonic as possible. So you'll find alot of familiarity with the default `logging` library. We even have the same set of logging functions that we can perform in the logging library.

Let us get started with...

## Installation

### with pip <small>recommended</small>
The updated stable version of monolg is maintained in **Python packing index** or [**PyPI**](https://pypi.org/project/monolg/) so it can easily be downloaded using `pip`. If you're using a virual environment like `venv` then inside the activated environment do the following

=== "Latest"
    ```bash
    $ pip install monolg
    ```
=== "`0.0.1`"
    ```bash
    $ pip intall monolg=="0.0.1"
    ```

### with github :fontawesome-brands-github:
Monolg can be downloaded directly from [**github**](https://github.com/Mukhopadhyay/monolg) as well, using the following command you'd be able to install monolg locally from the `master` branch

or you can install directly from github using.
```bash
$ pip install git+https://github.com/Mukhopadhyay/monolg.git@master
```

Comparing code with the `logging` module

=== "Using logging library"

    If you want to get started with logging using the built-in `logging` API provided by the standard library modules you would have to do the following

    ```python
    import logging

    # Setting up the logger
    logging.basicConfig(filename='test.log', level=logging.INFO)
    logging.info('Hello, World!')

    >>> INFO:root:Hello, World!
    ```

=== "Using `monolg`"

    Whereas, if we compare that to `Monolg` that is more if not as simpler,

    ```python
    from monolg import Monolg

    mlog = Monolg('mongodb://localhost:27017', verbose=True)
    mlog.conect()  # Connecting to the MongoDB instance
    mlog.info("Welcome to monolg")

    >>> 10-10-2022 10:10:10 [INFO] [system] monolg connected to mongodb
    >>> 10-10-2022 10:10:10 [INFO] [monolg] Welcome to monolg
    ```

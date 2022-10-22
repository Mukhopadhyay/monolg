# `monolg`
Centralized logging for Python using MongoDB

+ Licence: MIT License
+ Documentation: https://monolg.readthedocs.io/

## What is `monolg`?
You know those times when you've deployed your applications on the cloud, which logs every step of way precisely onto your `*.log` files, and now everytime you know the application misbehaves you cannot be bothered to look into those log files.

**This never happedn to you?!**

Let's not lie of course it has, and you know settings up Elastic stack will fix alot of your problems, but thats just ALOT OF WORK!!

That is where we want this project to come in, The monolg package should give you an easy to use API for logging all of your steps in your local MongoDB instance or even better your `MongoDB` Cloud (For which you know you have plenty out of those 512 MBs laying around)

## Installation

Monolg can be installed from PyPI using the following:

```bash
$ pip install monolg
```

## Getting started

```python
from monolg import Monolg

mlog = Monolg()
mlog.info("Welcome to monolg")
```

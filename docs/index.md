# monolg
Simple Centralized logging for Python using MongoDB

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com) [![ReadTheDocs](https://readthedocs.org/projects/monolg/badge/?version=latest)](https://monolg.readthedocs.io/en/latest/?version=latest)

[![PyPi](https://img.shields.io/pypi/v/monolg.svg)](https://pypi.python.org/pypi/monolg) [![Build Status](https://app.travis-ci.com/Mukhopadhyay/monolg.svg?branch=master)](https://app.travis-ci.com/Mukhopadhyay/monolg)

+ **Licence**: [**MIT License**](https://github.com/Mukhopadhyay/monolg/blob/master/LICENSE)
+ **Documentation**: [monolg.readthedocs.io](https://monolg.readthedocs.io)

## What is `monolg`?
You know those times when you've deployed your applications on the cloud, which logs every step of way precisely onto your `*.log` files, and now everytime you know the application misbehaves you cannot be bothered to look into those log files.

**This never happened to you?!**

Let's not lie of course it has, and you know settings up Elastic stack will fix alot of your problems, but thats just ALOT OF WORK!!

That is where we want this project to come in, The monolg package should give you an easy to use API for logging all of your steps in your local MongoDB instance or even better your `MongoDB` Cloud (For which you know you have plenty out of those 512 MBs laying around)


## Where can you use it?
You use `monolg` for pretty much any projects where you know keeping logs and sharing them is a necessary part. Granted it comes with an extra step of having a MongoDB instance up and running, but it does makes your life alot easier when it comes to identifying runtime issues, performance evaluations and debugging.


<!-- ## What it is not -->

.. monolg documentation master file, created by
   sphinx-quickstart on Mon Oct 17 22:43:00 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=====================================
Welcome to ``monolg``'s documentation
=====================================

Centralized logging for Python using MongoDB.
---------------------------------------------

|pypi| |readthedocs| |travis|

|prs-welcome|

.. |pyup|

..  toctree::
    :maxdepth: 2

    pages/getting-started
    pages/connecting-monolg
    pages/settings-and-configs
    pages/examples
    pages/tests
    pages/devs-note

* Licence: MIT License
* Documentation: https://monolg.readthedocs.io

What is monolg?
---------------
You know those times when you've deployed your applications
on the cloud, which logs every step of way precisely onto
your ``*.log`` files, and now everytime you know the application
misbehaves you cannot be bothered to look into those log files.

**This never happened to you?!**

Let's not lie of course it has, and you know settings up Elastic stack
will fix alot of your problems, but thats just ALOT OF WORK!!

That is where we want this project to come in, The `monolg` package
should give you an easy to use API for logging all of your steps
in your local MongoDB instance or even better your MongoDB
Cloud (For which you know you have plenty out of those 512 MBs laying around)

Installation
------------
Monolg can be installed from PyPI using the following:

.. sourcecode::

    pip install monolg


Getting started
---------------

Setting up the Monolg is almost as simple as setting up your built-in logger.
We can get started with logging with just the following few lines of code

.. image:: ./../images/simple.png


.. |prs-welcome| image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
    :target: https://makeapullrequest.com
    :alt: PRs Welcome

.. |pyup| image:: https://pyup.io/repos/github/Mukhopadhyay/monolg/shield.svg
    :target: https://pyup.io/repos/github/Mukhopadhyay/monolg/
    :alt: Updates

.. |readthedocs| image:: https://readthedocs.org/projects/monolg/badge/?version=latest
    :target: https://monolg.readthedocs.io/en/latest/?version=latest
    :alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/Mukhopadhyay/monolg.svg
    :target: https://travis-ci.com/Mukhopadhyay/monolg

.. |pypi| image:: https://img.shields.io/pypi/v/monolg.svg
    :target: https://pypi.python.org/pypi/monolg



.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

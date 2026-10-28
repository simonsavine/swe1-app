[![Build Status](https://app.travis-ci.com/simonsavine/swe1-app.svg?branch=main)](https://app.travis-ci.com/simonsavine/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/simonsavine/swe1-app/badge.svg)](https://coveralls.io/github/simonsavine/swe1-app)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# swe1-app

Django polls app (Hello World project), deployed to AWS Elastic Beanstalk by Travis CI.

Travis runs on every push and pull request: `black --check .`, `flake8 .`, then the test suite under `coverage`, reports coverage to Coveralls, and deploys `main` to Elastic Beanstalk when everything passes.

#!/bin/sh

pylint python_carrier_infinity/ tests/
mypy .
pytest -rP --cov=python_carrier_infinity

# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

# pylint: disable=missing-module-docstring

try:
    from .credentials import USERNAME, PASSWORD
except ImportError as exc:
    raise RuntimeError(
        "In order to run the tests, you must create a file named 'credentials.py'"
        + " containing 'USERNAME' and 'PASSWORD' variables."
    ) from exc

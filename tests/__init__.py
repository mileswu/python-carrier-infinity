# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

try:
    from .credentials import username, password
except ImportError as exc:
    raise Exception(
        "In order to run the tests, you must create a file named 'credentials.py' containing 'username' and 'password' variables."
    ) from exc

# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""updateInfinityConfig GraphQL schema"""
from __future__ import annotations

OPERATION = "updateInfinityConfig"
QUERY = """mutation updateInfinityConfig($input: InfinityConfigInput!) {
  updateInfinityConfig(input: $input) {
    etag
  }
}"""


def update_config_mode_query(
    serial: str,
    mode: str,
) -> dict:
    """Generate GraphQL query for updateInfinityConfig mode"""
    return {
        "operationName": OPERATION,
        "variables": {
            "input": {
                "serial": serial,
                "mode": mode,
            },
        },
        "query": QUERY,
    }

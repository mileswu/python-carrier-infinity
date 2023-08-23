# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""updateInfinityZoneActivity GraphQL schema"""
OPERATION = "updateInfinityZoneActivity"
QUERY = """mutation updateInfinityZoneActivity($input: InfinityZoneActivityInput!) {
  updateInfinityZoneActivity(input: $input) {
    etag
  }
}"""


def update_activity_temp_query(
    serial: str,
    zone_id: str,
    activity_type: str,
    target_cooling_temperature: int,
    target_heating_temperature: int,
) -> dict:
    """Generate GraphQL query for updateInfinityZoneActivity temperature"""

    return {
        "operationName": OPERATION,
        "variables": {
            "input": {
                "serial": serial,
                "zoneId": zone_id,
                "activityType": activity_type,
                "htsp": str(target_heating_temperature),
                "clsp": str(target_cooling_temperature),
            },
        },
        "query": QUERY,
    }


def update_activity_fan_query(
    serial: str, zone_id: str, activity_type: str, fan: str
) -> dict:
    """Generate GraphQL query for updateInfinityZoneActivity fan"""

    return {
        "operationName": OPERATION,
        "variables": {
            "input": {
                "serial": serial,
                "zoneId": zone_id,
                "activityType": activity_type,
                "fan": fan,
            },
        },
        "query": QUERY,
    }

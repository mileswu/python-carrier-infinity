"""updateInfinityZoneConfig GraphQL schema"""
from __future__ import annotations

OPERATION = "updateInfinityZoneConfig"
QUERY = """mutation updateInfinityZoneConfig($input: InfinityZoneConfigInput!) {
  updateInfinityZoneConfig(input: $input) {
    etag
  }
}"""


def update_zone_config_query(
    serial: str,
    zone_id: str,
    hold_activity: str | None,
    hold_until: str | None,
) -> dict:
    """Generate GraphQL query for updateInfinityZoneConfig"""

    if hold_activity:
        hold = "on"
    else:
        hold = "off"

    return {
        "operationName": OPERATION,
        "variables": {
            "input": {
                "serial": serial,
                "zoneId": zone_id,
                "hold": hold,
                "holdActivity": hold_activity,
                "otmr": hold_until,
            },
        },
        "query": QUERY,
    }

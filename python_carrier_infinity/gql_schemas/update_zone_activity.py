operation = "updateInfinityZoneActivity"
query = """mutation updateInfinityZoneActivity($input: InfinityZoneActivityInput!) {
  updateInfinityZoneActivity(input: $input) {
    etag
  }
}"""


def update_zone_activity_query(system_id, zone_id, activity_type, cool_temp, heat_temp):
    return {
        "operationName": operation,
        "variables": {
            "input": {
                "serial": system_id,
                "zoneId": zone_id,
                "activityType": activity_type,
                "htsp": str(heat_temp),
                "clsp": str(cool_temp),
            },
        },
        "query": query,
    }

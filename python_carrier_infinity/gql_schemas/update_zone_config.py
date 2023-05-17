operation = "updateInfinityZoneConfig"
query = """mutation updateInfinityZoneConfig($input: InfinityZoneConfigInput!) {
  updateInfinityZoneConfig(input: $input) {
    etag
  }
}"""

def update_zone_config_query(system_id, zone_id, hold, hold_activity, otmr):
    return {
        "operationName": operation,
        "variables": {
            "input": {
                "serial": system_id,
                "zoneId": zone_id,
                "hold": hold,
                "holdActivity": hold_activity,
                "otmr": otmr #The time by which the hold expires; None if hold is indefinite
            },
        },
        "query": query
    }

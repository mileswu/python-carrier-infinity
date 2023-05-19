"""getInfinityStatus GraphQL schema"""

OPERATION = "getInfinityStatus"
QUERY_FULL = """query getInfinityStatus($serial: String!) {
  infinityStatus(serial: $serial) {
    localTime
    localTimeOffset
    utcTime
    wcTime
    isDisconnected
    cfgem
    mode
    vacatrunning
    oat
    odu {
      type
      opstat
    }
    filtrlvl
    idu {
      type
      opstat
      cfm
    }
    vent
    ventlvl
    humid
    humlvl
    uvlvl
    zones {
      id
      rt
      rh
      fan
      htsp
      clsp
      hold
      enabled
      currentActivity
    }
  }
}"""

QUERY = """query getInfinityStatus($serial: String!) {
  infinityStatus(serial: $serial) {
    utcTime
    cfgem
    mode
    oat
    odu {
      type
      opstat
    }
    idu {
      type
      opstat
      cfm
    }
    humid
    zones {
      id
      rt
      rh
      fan
      htsp
      clsp
      hold
      enabled
      currentActivity
    }
  }
}"""


def get_status_query(serial: str) -> dict:
    """Generate GraphQL query for getInfinityStatus"""
    return {
        "operationName": OPERATION,
        "variables": {"serial": serial},
        "query": QUERY,
    }

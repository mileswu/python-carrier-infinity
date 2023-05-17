operation = "getInfinityStatus"
query_long = """query getInfinityStatus($serial: String!) {
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

query = """query getInfinityStatus($serial: String!) {
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
def get_system_status_query(system_id):
    return {
        "operationName": operation,
        "variables": {
            "serial": system_id
        },
        "query": query,
    }
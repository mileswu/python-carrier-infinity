operation = "getInfinityConfig"
query_long = """query getInfinityConfig($serial: String!) {
  infinityConfig(serial: $serial) {
    etag
    mode
    cfgem
    cfgdead
    cfghumid
    erate
    grate
    heatsource
    vacat
    vacstart
    vacend
    vacmint
    vacmaxt
    vacfan
    fueltype
    gasunit
    cfgvent
    cfghumid
    cfguv
    cfgfan
    vacat
    filtertype
    filterinterval
    humidityVacation {
      rclgovercool
      ventspdclg
      ventclg
      rhtg
      humidifier
      humid
      venthtg
      rclg
      ventspdhtg
    }
    zones {
      id
      name
      enabled
      hold
      holdActivity
      otmr
      program {
        id
        day {
          id
          zoneId
          period {
            id
            zoneId
            dayId
            activity
            time
            enabled
          }
        }
      }
      activities {
        id
        zoneId
        type
        fan
        previousFan
        htsp
        clsp
      }
    }
    wholeHouse {
      hold
      holdActivity
      otmr
      activities {
        id
        htsp
        clsp
        fan
      }
    }
    humidityAway {
      humid
      humidifier
      rhtg
      rclg
      rclgovercool
    }
    humidityHome {
      humid
      humidifier
      rhtg
      rclg
      rclgovercool
    }
  }
}
"""

query = """query getInfinityConfig($serial: String!) {
  infinityConfig(serial: $serial) {
    mode
    cfgem
    zones {
      id
      name
      enabled
      hold
      holdActivity
      otmr
      activities {
        id
        zoneId
        type
        fan
        previousFan
        htsp
        clsp
      }
    }
  }
}
"""

def get_system_config_query(system_id):
    return {
        "operationName": operation,
        "variables": {
            "serial": system_id,
        },
        "query": query
    }

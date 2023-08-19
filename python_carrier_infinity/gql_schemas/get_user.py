# SPDX-FileCopyrightText: 2022-present @mileswu <mileswu@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""getUser GraphQL schema"""
OPERATION = "getUser"
QUERY = """query getUser(
    $userName: String!,
    $appVersion: String,
    $brand: String,
    $os: String,
    $osVersion: String) {
  user(
    userName: $userName
    appVersion: $appVersion
    brand: $brand
    os: $os
    osVersion: $osVersion
  ) {
    username
    first
    last
    email
    emailVerified
    secondaryEmail
    secondaryEmailVerified
    phone1
    acceptedTermsOfServiceDateTime
    creationSource
    postal
    locations {
      locationId
      name
      street1
      street2
      city
      state
      country
      postal
      systems {
        profile {
          serial
          name
          firmware
          model
          idutype
        }
      }
      devices {
        deviceId
        type
        tempUnit
      }
    }
    betaConfiguration {
      status
      features {
        featureId
        isActive
        config {
          configId
          configValue
        }
      }
    }
  }
}
"""


def get_user_query(username: str) -> dict:
    """Generate GraphQL query for getUser"""
    return {
        "operationName": OPERATION,
        "variables": {
            "userName": username,
            "appVersion": "1.6.3-21321",
            "brand": "Carrier",
            "os": "ios",
            "osVersion": "16.4.1",
        },
        "query": QUERY,
    }

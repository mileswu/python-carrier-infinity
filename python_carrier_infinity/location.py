"""Contains the Location class"""

from xml.etree.ElementTree import Element
from . import util


class Location(object):
    """Represents a location"""

    def __init__(self, data: dict):
        self.location_id = data["locationId"]
        self.name = data["name"]
        self.street1 = data["street1"]
        self.street2 = data["street2"]
        self.city = data["city"]
        self.state = data["state"]
        self.country = data["country"]
        self.postal = data["postal"]

    # for testing
    def __str__(self):
        return f"""
            Location Id: {self.location_id}
            Name: {self.name}
            Postal: {self.postal}
        """

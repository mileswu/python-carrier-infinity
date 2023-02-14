"""Contains the System class"""
from xml.etree.ElementTree import Element
import defusedxml.ElementTree as ET
from . import util
from . import api
from .api import Auth
from .config import Config
from .location import Location
from .status import Status


class System(object):
    """Represents a Carrier Infinity system"""

    def __init__(self, xml: Element, location: Location, auth: api.Auth):
        link_xml = util.get_xml_element(xml, "{http://www.w3.org/2005/Atom}link")
        self.system_id = util.get_xml_attribute(link_xml, "href").split("/")[-1]
        self.name = util.get_xml_attribute(link_xml, "title")
        self.auth = auth
        self.location = location

    async def status(self) -> "Status":
        """Fetch current system status"""
        response = await api.request(
            f"/systems/{self.system_id}/status", None, self.auth
        )
        xml = ET.fromstring(response)
        return Status(xml)

    async def config(self) -> "Config":
        """Fetch the current config of the system"""
        response = await api.request(
            f"/systems/{self.system_id}/config", None, self.auth
        )
        xml = ET.fromstring(response)
        return Config(xml)


async def systems(auth: Auth) -> list[System]:
    """Fetch list of all systems"""
    response = await api.request(f"/users/{auth.username}/locations", None, auth)
    all_systems = []
    xml = ET.fromstring(response)
    for location_xml in xml.iter("location"):
        loc = Location(location_xml)
        for system_xml in location_xml.iter("system"):
            all_systems.append(System(system_xml, loc, auth))

    return all_systems

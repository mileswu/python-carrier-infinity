"""Contains the Location class"""

from xml.etree.ElementTree import Element
from . import util


class Location(object):
    """Represents a location"""

    def __init__(self, xml: Element):
        link_xml = util.get_xml_element(xml, "{http://www.w3.org/2005/Atom}link")
        self.location_id = util.get_xml_attribute(link_xml, "href").split("/")[-1]
        self.name = util.get_xml_element(xml, "name").text
        self.street1 = util.get_xml_element(xml, "street1").text
        self.street2 = util.get_xml_element(xml, "street2").text
        self.city = util.get_xml_element(xml, "city").text
        self.state = util.get_xml_element(xml, "state").text
        self.country = util.get_xml_element(xml, "country").text
        self.postal = util.get_xml_element(xml, "postal").text

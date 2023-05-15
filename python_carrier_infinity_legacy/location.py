"""Contains the Location class"""

from xml.etree.ElementTree import Element
from . import util


class Location(object):
    """Represents a location"""

    def __init__(self, xml: Element):
        link_xml = util.get_xml_element(xml, "{http://www.w3.org/2005/Atom}link")
        self.location_id = util.get_xml_attribute(link_xml, "href").split("/")[-1]
        self.name = util.get_xml_element_text(xml, "name")
        self.street1 = util.get_xml_element_text(xml, "street1")
        self.street2 = util.get_xml_element_text(xml, "street2")
        self.city = util.get_xml_element_text(xml, "city")
        self.state = util.get_xml_element_text(xml, "state")
        self.country = util.get_xml_element_text(xml, "country")
        self.postal = util.get_xml_element_text(xml, "postal")

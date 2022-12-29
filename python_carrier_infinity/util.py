"""Utility functions"""
from xml.etree.ElementTree import tostring as xml_tostring
from xml.etree.ElementTree import Element


def get_xml_element(xml: Element, tag: str) -> Element:
    """Get a single instance of an XML element by tag"""

    try:
        result = next(xml.iter(tag))
    except StopIteration as exc:
        raise Exception(f"<{tag}> could not be found in {xml_tostring(xml)}") from exc
    return result


def get_xml_attribute(xml: Element, key: str) -> str:
    """Get an attribute from an XML element"""
    result = xml.get(key)
    if result is None:
        raise Exception(f"'{key}' attribute could not be found in {xml_tostring(xml)}")
    else:
        return result

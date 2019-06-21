import os
from bs4 import BeautifulSoup
from edinet.parser.xbrl_element import XBRLValue, XBRLDocument


class XBRLFile():

    def __init__(self, path):
        self.path = path

    def get_element(self, tag):
        if not os.path.exists(self.path):
            raise FileNotFoundError()

        element = None
        with open(self.path, encoding="utf-8") as f:
            root = BeautifulSoup(f, "lxml-xml")
            element = root.find(tag)

        return element

    def get_value(self, tag):
        element = self.get_element(tag)
        return XBRLValue(element)

    def get_document(self, tag):
        element = self.get_element(tag)
        return XBRLDocument(element)

    def get_executive_state(self):
        from edinet.parser.aspects.executive_state import ExecutiveStateParser
        parser = ExecutiveStateParser(self)
        return parser.parse()

from edinet.parser.xbrl_parser import XBRLParser
from edinet.document.xbrl_value import XBRLValue


class BaseAspect():
    TAGS = {}

    def __init__(self, reader):
        self.reader = reader

    def find(self, name):
        tag = self.TAGS[name]
        element = self.reader.xbrl.find(tag)
        if element is None:
            without_ns = tag.split(":")[1]  # without ns
            element = self.reader.xbrl.find(without_ns)

        if element:
            element = self.reader._to_element(element)
            return element
        else:
            return None

    def get_parser(self, name):
        element = self.find(name)
        if element:
            return XBRLParser(element)
        else:
            return None

    def get_text_value(self, name):
        element = self.find(name)
        parser = XBRLParser()
        if element is not None:
            html = element.html
            raw = html.prettify()
            value = parser.normalize(html.text)
            value = XBRLValue.text(value=value, ground=raw)
            return value
        else:
            return None

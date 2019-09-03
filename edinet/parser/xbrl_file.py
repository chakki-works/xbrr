import os
from bs4 import BeautifulSoup


class XBRLFile():

    def __init__(self, path):
        self.path = path
        self._root = None

        # Load XBRL file
        if not os.path.exists(self.path):
            raise FileNotFoundError()

        with open(self.path, encoding="utf-8") as f:
            self._root = BeautifulSoup(f, "lxml-xml")

    @property
    def text(self):
        return self._root.text

    def find(self, tag):
        tag_element = self._root.find(tag)
        return XBRLElement(tag_element)

    def parse_by(self, parser_cls):
        return parser_cls(self._root)


class XBRLElement():

    def __init__(self, element):
        self._element = element

    @property
    def text(self):
        return self._element.text

    def find(self, tag):
        tag_element = self._element.find(tag)
        return XBRLElement(tag_element)

    def to_html(self):
        _text = self._element.text.strip()
        html_text = _text.replace("&lt;", "<").replace("&gt;", ">")
        html = BeautifulSoup(html_text, "html.parser")
        return XBRLElement(html)

    def parse_by(self, parser_cls):
        return parser_cls(self._element)

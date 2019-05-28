from bs4 import BeautifulSoup
from edinet.parser.xbrl_element_reader import XBRLElementReader


class XBRLValue():

    def __init__(self, element):
        self.tree = element

    @property
    def text(self):
        _text = self.tree.text
        return _text.strip()


class XBRLDocument():

    def __init__(self, element):
        self.tree = element
        self.reader = XBRLElementReader(self.tree)

    @property
    def html(self):
        _text = self.tree.text.strip()
        html_text = _text.replace("&lt;", "<").replace("&gt;", ">")
        html = BeautifulSoup(html_text, "html.parser")
        return XBRLDocument(html)

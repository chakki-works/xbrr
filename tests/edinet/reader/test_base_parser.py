import os
import re
import unittest
from xbrr.edinet.reader.reader import Reader
from xbrr.base.reader.base_parser import BaseParser
from xbrr.edinet.reader.element import Element


class TestBaseParser(unittest.TestCase):

    def test_search_text(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/xbrl2019.xbrl")
        reader = Reader(path)
        tag = "jpcrp_cor:InformationAboutOfficersTextBlock"
        parser = BaseParser(reader, Element, {
            "test": tag
        })
        pattern = "^(男性).+(名).+(女性).+(名)"
        text = parser.search("test", pattern)
        self.assertEqual(text, "男性 13名 女性 1名 (役員のうち女性の比率 7.1%)")

    def test_extract_value(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/xbrl2019.xbrl")
        reader = Reader(path)
        tag = "jpcrp_cor:InformationAboutOfficersTextBlock"
        parser = BaseParser(reader, Element, {
            "test": tag
        })
        pattern = "^(男性).+(名).+(女性).+(名)"
        for p, s in [("男性", "名"), ("女性", "名"), ("女性の比率", "%")]:
            value = parser.extract_value("test", p, s, filter_pattern=pattern)
            if p == "男性":
                self.assertEqual(value, 13)
            elif p == "女性":
                self.assertEqual(value, 1)
            else:
                self.assertEqual(value, 7.1)

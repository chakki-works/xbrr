import os
import re
import unittest
from edinet.xbrl_file import XBRLFile
from edinet.parser.xbrl_parser import XBRLParser


class TestXBRLParser(unittest.TestCase):

    def test_search_text(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/xbrl2019.xbrl")
        xbrl = XBRLFile(path)
        tag = "jpcrp_cor:InformationAboutOfficersTextBlock"
        pattern = "^(男性).+(名).+(女性).+(名)"
        text = xbrl.find(tag).to_html().parse_by(XBRLParser).search_text(pattern)
        self.assertEqual(text, "男性 13名 女性 1名 (役員のうち女性の比率 7.1%)")

    def test_extract_value(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/xbrl2019.xbrl")
        xbrl = XBRLFile(path)
        tag = "jpcrp_cor:InformationAboutOfficersTextBlock"
        pattern = "^(男性).+(名).+(女性).+(名)"
        for p, s in [("男性", "名"), ("女性", "名"), ("女性の比率", "%")]:
            value = xbrl.find(tag) \
                    .to_html() \
                    .parse_by(XBRLParser) \
                    .extract_value(p, s, filter_pattern=pattern)

            if p == "男性":
                self.assertEqual(value, 13)
            elif p == "女性":
                self.assertEqual(value, 1)
            else:
                self.assertEqual(value, 7.1)

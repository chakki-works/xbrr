import os
import re
import unittest
from edinet.parser.xbrl_file import XBRLFile
import edinet.parser.item_extractor as ie


class TestItemExtractor(unittest.TestCase):

    def test_text_context_matcher(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        document = xbrl.get_document("jpcrp_cor:InformationAboutOfficersTextBlock")

        matcher = ie.TextContextMatcher("^(男性).+(名).+(女性).+(名)")
        text = matcher.search(document.html)
        self.assertEqual(text, "男性　13名　女性　1名　（役員のうち女性の比率　7.1％）")

    def test_text_value_extractor(self):
        for p, s in [("男性", "名"), ("女性", "名"), ("女性の比率", "％")]:
            extractor = ie.TextValueExtractor(p, s)
            value = extractor.extract("男性　13名　女性　1名　（役員のうち女性の比率　7.1％）")
            if p == "男性":
                self.assertEqual(value, 13)
            elif p == "女性":
                self.assertEqual(value, 1)
            else:
                self.assertEqual(value, 7.1)

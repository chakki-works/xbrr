import os
import re
import unittest
from edinet.reader.edinet.xbrl_reader import XBRLReader


class TestXBRLReader(unittest.TestCase):

    def test_find(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/xbrl2019.xbrl")
        xbrl = XBRLReader(path)
        element = xbrl.find("jpdei_cor:EDINETCodeDEI")
        self.assertEqual(element.text, "E05739")

    def test_to_html(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/xbrl2019.xbrl")
        xbrl = XBRLReader(path)
        tag = "jpcrp_cor:InformationAboutOfficersTextBlock"
        html = xbrl.find(tag).html

        self.assertTrue(html)

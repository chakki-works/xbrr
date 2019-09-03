import os
import unittest
from edinet.parser.xbrl_file import XBRLFile


class TestXBRLFile(unittest.TestCase):

    def test_find(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        element = xbrl.find("jpdei_cor:EDINETCodeDEI")
        self.assertEqual(element.text, "E05739")

    def test_to_html(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        tag = "jpcrp_cor:InformationAboutOfficersTextBlock"
        html = xbrl.find(tag).to_html()

        self.assertTrue(html)

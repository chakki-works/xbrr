import os
import unittest
from edinet.parser.xbrl_file import XBRLFile


class TestXBRLFile(unittest.TestCase):

    def test_get_value(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        value = xbrl.get_value("jpdei_cor:EDINETCodeDEI")
        self.assertTrue(value)
        self.assertEqual(value.text, "E05739")

    def test_get_document(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        document = xbrl.get_document("jpcrp_cor:InformationAboutOfficersTextBlock")

        self.assertTrue(document.html)

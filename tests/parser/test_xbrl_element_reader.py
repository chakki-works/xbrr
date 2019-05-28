import os
import re
import unittest
from edinet.parser.xbrl_file import XBRLFile


class TestXBRLElementReader(unittest.TestCase):

    def test_find_text(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        document = xbrl.get_document("jpcrp_cor:InformationAboutOfficersTextBlock")
        text = document.html.reader.find_text(re.compile("^(男性).+(名).+(女性).+(名)"))
        self.assertTrue(text)
        self.assertFalse(True)

import os
import unittest
from edinet.parser.xbrl_file import XBRLFile


class TestExecutiveState(unittest.TestCase):

    def test_parse(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        executive_state = xbrl.get_executive_state()
        self.assertTrue(executive_state)

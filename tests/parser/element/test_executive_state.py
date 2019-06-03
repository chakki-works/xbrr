import os
import unittest
from edinet.parser.xbrl_file import XBRLFile
from edinet.parser.element.executive_state import ExecutiveState


class TestExecutiveState(unittest.TestCase):

    def test_number_of_executives(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        executive_state = ExecutiveState(xbrl)
        self.assertEqual(executive_state.number_of_executives[0], 14)

    def test_percentage_of_female_executives(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        executive_state = ExecutiveState(xbrl)
        self.assertEqual(executive_state.percentage_of_female_executives[0], 1 / 14)

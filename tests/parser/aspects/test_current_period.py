import os
import unittest
from edinet.parser.xbrl_file import XBRLFile
from edinet.parser.aspects.current_period import CurrentPeriod


class TestCurrentPeriod(unittest.TestCase):

    def test_fiscal_year(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        current_period = CurrentPeriod(xbrl)
        self.assertEqual(current_period.fiscal_year.value, 2017)

    def test_fiscal_period_type(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        current_period = CurrentPeriod(xbrl)
        self.assertEqual(current_period.fiscal_period_type.value, "FY")

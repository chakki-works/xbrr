import os
import unittest
from edinet.parser.xbrl_file import XBRLFile
from edinet.parser.aspects.finance import Finance


class TestFinance(unittest.TestCase):

    def get_xbrl(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/xbrl2019.xbrl")
        xbrl = XBRLFile(path)
        return xbrl

    def test_voluntary_accounting_policy_change(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Finance).voluntary_accounting_policy_change

    def test_segment_information(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Finance).segment_information
        self.assertTrue(feature.value.startswith("(セグメント情報等)"))

    def test_real_estate_for_lease(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Finance).real_estate_for_lease

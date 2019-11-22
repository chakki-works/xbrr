import os
import unittest
from edinet.reader.edinet.xbrl_reader import XBRLReader
from edinet.reader.edinet.aspects.finance import Finance


class TestFinance(unittest.TestCase):

    def get_xbrl(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../../data/xbrl2019.xbrl")
        xbrl = XBRLReader(path)
        return xbrl

    def test_voluntary_accounting_policy_change(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Finance).voluntary_accounting_policy_change

    def test_segment_information(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Finance).segment_information
        self.assertTrue(feature.normalized_text.startswith("(セグメント情報等)"))

    def test_real_estate_for_lease(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Finance).real_estate_for_lease

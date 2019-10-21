import os
import unittest
from edinet.xbrl_file import XBRLFile
from edinet.parser.aspects.information import Information


class TestInformation(unittest.TestCase):

    def get_xbrl(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/xbrl2019.xbrl")
        xbrl = XBRLFile(path)
        return xbrl

    def test_shareholders(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Information).shareholders
        self.assertTrue(feature.value.startswith("(5)【所有者別状況】"))

    def test_dividend_policy(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Information).dividend_policy
        self.assertTrue(feature.value.startswith("3【配当政策】"))

    def test_directors(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Information).directors
        self.assertTrue(feature.value.startswith("5【役員の状況】"))

    def test_corporate_governance(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Information).corporate_governance
        self.assertTrue(feature.value.startswith("(1)【コーポレート・ガバナンスの状況】"))

    def test_number_of_executives(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Information).number_of_directors
        self.assertEqual(feature.value, 14)

    def test_number_of_female_executives(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Information).number_of_female_executives
        self.assertEqual(feature.value, 1)

import os
import unittest
from edinet.parser.xbrl_file import XBRLFile
from edinet.parser.aspects.information_about_company import InformationAboutCompany


class TestInformationAboutCompany(unittest.TestCase):

    def get_xbrl(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        return xbrl

    def test_shareholders(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(InformationAboutCompany).shareholders
        self.assertTrue(feature.value.startswith("(5)【所有者別状況】"))

    def test_dividend_policy(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(InformationAboutCompany).dividend_policy
        self.assertTrue(feature.value.startswith("3【配当政策】"))

    def test_directors(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(InformationAboutCompany).directors
        self.assertTrue(feature.value.startswith("5【役員の状況】"))

    def test_corporate_governance(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(InformationAboutCompany).corporate_governance
        self.assertTrue(feature.value.startswith("(1)【コーポレート・ガバナンスの状況】"))

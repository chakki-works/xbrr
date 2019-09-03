import os
import unittest
from edinet.parser.xbrl_file import XBRLFile
from edinet.parser.aspects.business import Business


class TestBusiness(unittest.TestCase):

    def get_xbrl(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/test_example_1.xbrl")
        xbrl = XBRLFile(path)
        return xbrl

    def test_policy_environment_issue_etc(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Business).policy_environment_issue_etc
        print(feature.value)
        self.assertTrue(feature.value.startswith("1【経営方針、経営環境及び対処すべき課題等】"))

    def test_risks(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Business).risks
        print(feature.value)
        self.assertTrue(feature.value.startswith("2【事業等のリスク】"))

    def test_research_and_development(self):
        xbrl = self.get_xbrl()
        feature = xbrl.parse_by(Business).research_and_development
        print(feature.value)
        self.assertTrue(feature.value.startswith("5【研究開発活動】"))

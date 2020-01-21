import os
import unittest
from xbrr.edinet.reader.reader import Reader
from xbrr.edinet.reader.aspects.business import Business


class TestBusiness(unittest.TestCase):

    def get_xbrl(self, year=2019):
        path = os.path.join(os.path.dirname(__file__),
                            f"../../data/xbrl{year}.xbrl")
        xbrl = Reader(path)
        return xbrl

    def test_policy_environment_issue_etc(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Business).policy_environment_issue_etc
        self.assertTrue(feature.normalized_text.startswith("1【経営方針、経営環境及び対処すべき課題等】"))

    def test_risks(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Business).risks
        self.assertTrue(feature.normalized_text.startswith("2【事業等のリスク】"))

    def test_management_analysis(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Business).management_analysis
        self.assertTrue(feature.normalized_text.startswith("3【経営者による財政状態、経営成績及びキャッシュ・フローの状況の分析】"))

    def test_research_and_development(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Business).research_and_development
        self.assertTrue(feature.normalized_text.startswith("5【研究開発活動】"))

    def test_overview_of_result(self):
        xbrl = self.get_xbrl(2018)
        feature = xbrl.extract(Business).overview_of_result
        self.assertTrue(feature.normalized_text.startswith("1【業績等の概要】"))

    def test_overview_of_value_chain(self):
        xbrl = self.get_xbrl(2018)
        feature = xbrl.extract(Business).overview_of_value_chain
        self.assertTrue(feature.normalized_text.startswith("2【生産、受注及び販売の状況】"))

    def test_analysis_of_finance(self):
        xbrl = self.get_xbrl(2018)
        feature = xbrl.extract(Business).analysis_of_finance
        self.assertTrue(feature.normalized_text.startswith("7【財政状態、経営成績及びキャッシュ・フローの状況の分析】"))

import os
import unittest
from xbrr.edinet.reader.reader import Reader
from xbrr.edinet.reader.aspects.company import Company


class TestCompany(unittest.TestCase):

    def get_xbrl(self):
        path = os.path.join(os.path.dirname(__file__),
                            "../../data/xbrl2019.xbrl")
        xbrl = Reader(path)
        return xbrl

    def test_history(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Company).history
        self.assertTrue(feature.normalized_text.startswith("2【沿革】"))

    def test_business_description(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Company).business_description
        self.assertTrue(feature.normalized_text.startswith("3【事業の内容】"))

    def test_affiliated_entities(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Company).affiliated_entities
        self.assertTrue(feature.normalized_text.startswith("4【関係会社の状況】"))

    def test_employees(self):
        xbrl = self.get_xbrl()
        feature = xbrl.extract(Company).employees
        self.assertTrue(feature.normalized_text.startswith("5【従業員の状況】"))

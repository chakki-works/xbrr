import os
import shutil
import unittest
from xbrr.edinet.client.document_client import DocumentClient
from xbrr.edinet.reader.reader import Reader
from xbrr.edinet.reader.aspects.company import Company


class TestCompany(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _dir = os.path.join(os.path.dirname(__file__), "../../data")
        client = DocumentClient()
        file_path = client.get_xbrl("S100G70J", save_dir=_dir,
                                    expand_level="dir")
        cls.reader = Reader(file_path)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.reader.xbrl_dir.root)
        if os.path.exists(cls.reader.taxonomy.root):
            shutil.rmtree(cls.reader.taxonomy.root)

    def test_history(self):
        feature = self.reader.extract(Company).history
        self.assertTrue(feature.normalized_text.startswith("2【沿革】"))

    def test_business_description(self):
        feature = self.reader.extract(Company).business_description
        self.assertTrue(feature.normalized_text.startswith("3【事業の内容】"))

    def test_affiliated_entities(self):
        feature = self.reader.extract(Company).affiliated_entities
        self.assertTrue(feature.normalized_text.startswith("4【関係会社の状況】"))

    def test_employees(self):
        feature = self.reader.extract(Company).employees
        self.assertTrue(feature.normalized_text.startswith("5【従業員の状況】"))

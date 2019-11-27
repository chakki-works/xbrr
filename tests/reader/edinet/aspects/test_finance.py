import os
import shutil
import unittest
from edinet.client.document_client import DocumentClient
from edinet.reader.edinet.xbrl_reader import XBRLReader
from edinet.reader.edinet.aspects.finance import Finance


class TestFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _dir = os.path.join(os.path.dirname(__file__), "../../../data")
        client = DocumentClient()
        file_path = client.get_xbrl("S100G2KL", save_dir=_dir,
                                    expand_level="dir")
        cls.reader = XBRLReader(file_path)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.reader.xbrl_dir.root)
        if os.path.exists(cls.reader.taxonomy.root):
            shutil.rmtree(cls.reader.taxonomy.root)

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

    def test_bs(self):
        bs = self.reader.extract(Finance).bs()
        self.assertGreater(len(bs), 0)

    def test_pl(self):
        pl = self.reader.extract(Finance).pl()
        self.assertGreater(len(pl), 0)

    def test_bs_ifrs(self):
        bs = self.reader.extract(Finance).bs(ifrs=True)
        self.assertGreater(len(bs), 0)

    def test_pl_ifrs(self):
        pl = self.reader.extract(Finance).pl(ifrs=True)
        self.assertGreater(len(pl), 0)

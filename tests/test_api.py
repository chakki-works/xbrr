import os
import time
import unittest
import edinet
from tests.utils import delay


class TestAPI(unittest.TestCase):

    @delay
    def ztest_api_metadata(self):
        metadata = edinet.api.metadata.get("2019-01-31")
        self.assertGreater(metadata.count, 0)

    @delay
    def ztest_api_document(self):
        _dir = os.path.dirname(__file__)
        path = edinet.api.document.get_pdf("S100FGR9", save_dir=_dir)
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    @delay
    def test_api_documents(self):
        documents = edinet.api.documents.get("2019-02-01")
        self.assertEqual(documents.metadata.count, len(documents.list))

        _dir = os.path.dirname(__file__)
        d = documents.list[0]
        for ext in ["xbrl", "pdf"]:
            time.sleep(3)
            if ext == "xbrl":
                path = d.get_xbrl(save_dir=_dir)
            else:
                path = d.get_pdf(save_dir=_dir)

            self.assertTrue(os.path.exists(path))
            os.remove(path)

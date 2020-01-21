import os
import time
import unittest
import xbrr
from tests.utils import delay


class TestAPI(unittest.TestCase):

    @delay
    def test_api_metadata(self):
        metadata = xbrr.edinet.api.metadata.get("2019-01-31")
        self.assertGreater(metadata.count, 0)

    @delay
    def test_api_document(self):
        _dir = os.path.dirname(__file__)
        path = xbrr.edinet.api.document.get_pdf("S100FGR9", save_dir=_dir)
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    @delay
    def test_api_documents(self):
        documents = xbrr.edinet.api.documents.get("2019-02-01")
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

    def test_extract(self):
        path = os.path.join(os.path.dirname(__file__),
                            "./data/xbrl2019.xbrl")

        result = xbrr.edinet.reader.read(path).extract(
                    xbrr.edinet.aspects.Business).policy_environment_issue_etc
        self.assertTrue(result.value)

    def test_extract_element(self):
        path = os.path.join(os.path.dirname(__file__),
                            "./data/xbrl2019.xbrl")

        result = xbrr.edinet.reader.read(path).extract("information", "number_of_directors")
        self.assertEqual(result.value, 14)

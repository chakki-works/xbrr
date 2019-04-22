import os
import unittest
from edinet.client.document_client import DocumentClient
from tests.utils import delay


class TestDocumentClient(unittest.TestCase):

    @delay
    def test_get(self):
        _dir = os.path.dirname(__file__)
        client = DocumentClient()
        file_path = client.get("S100FGR9", response_type=1, save_dir=_dir)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

    @delay
    def test_get_pdf(self):
        _dir = os.path.dirname(__file__)
        client = DocumentClient()
        file_path = client.get_pdf("S100FGR9", save_dir=_dir)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

    @delay
    def test_get_xbrl(self):
        _dir = os.path.dirname(__file__)
        client = DocumentClient()
        # lang="en" does not exist?
        file_path = client.get_xbrl("S100FGR9", save_dir=_dir)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

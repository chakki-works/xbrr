import os
import shutil
import unittest
from xbrr.edinet.client.document_client import DocumentClient
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

    @delay
    def test_get_xbrl_zip(self):
        _dir = os.path.dirname(__file__)
        client = DocumentClient()
        # lang="en" does not exist?
        file_path = client.get_xbrl("S100FGR9", save_dir=_dir,
                                    expand_level="dir")
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isdir(file_path))
        shutil.rmtree(file_path)

    @delay
    def test_get_xbrl_zip_dir(self):
        _dir = os.path.dirname(__file__)
        client = DocumentClient()
        # lang="en" does not exist?
        file_path = client.get_xbrl("S100FGSC", save_dir=_dir,
                                    expand_level=None)
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(str(file_path).endswith(".zip"))
        os.remove(file_path)

    @delay
    def test_get_pdf_without_dir(self):
        client = DocumentClient()
        file_path = client.get_pdf("S100FGR9")
        self.assertTrue(os.path.exists(file_path))
        name = os.path.basename(file_path)
        self.assertTrue(str(name).startswith("S100FGR9_2__"))
        self.assertTrue(str(name).endswith(".pdf"))
        os.remove(file_path)

import os
import unittest
from xbrr.edinet.models import Document
from tests.utils import delay


class TestDocument(unittest.TestCase):

    @delay
    def test_document_get_xbrl(self):
        _dir = os.path.dirname(__file__)
        d = Document(document_id="S100FGR9")
        path = d.get_xbrl(save_dir=_dir)
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    @delay
    def test_document_get_pdf(self):
        _dir = os.path.dirname(__file__)
        d = Document(document_id="S100FGR9")
        path = d.get_pdf(save_dir=_dir)
        self.assertTrue(os.path.exists(path))
        os.remove(path)

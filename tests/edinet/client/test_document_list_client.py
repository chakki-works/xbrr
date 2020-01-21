import unittest
from datetime import datetime
from xbrr.edinet.client.document_list_client import MetaDataClient
from xbrr.edinet.client.document_list_client import DocumentListClient
from tests.utils import delay


class TestDocumentListClient(unittest.TestCase):

    @delay
    def test_metadata(self):
        client = MetaDataClient()
        metadata = client.get("2019-01-31")
        self.assertGreater(metadata.count, 0)

    @delay
    def test_metadata_by_datetime(self):
        client = MetaDataClient()
        date = datetime(2019, 3, 1)
        metadata = client.get(date)
        self.assertGreater(metadata.count, 0)

    @delay
    def test_document_list(self):
        client = DocumentListClient()
        documents = client.get("2019-01-31")
        self.assertEqual(documents.metadata.count, len(documents.list))

    @delay
    def test_document_list_by_datetime(self):
        client = DocumentListClient()
        date = datetime(2019, 3, 1)
        documents = client.get(date)
        self.assertEqual(documents.metadata.count, len(documents.list))

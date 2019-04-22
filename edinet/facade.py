from edinet.client.document_list_client import MetaDataClient
from edinet.client.document_list_client import DocumentListClient
from edinet.client.document_client import DocumentClient


class Facade():

    @property
    def metadata(self):
        client = MetaDataClient()
        return client

    @property
    def documents(self):
        client = DocumentListClient()
        return client

    @property
    def document(self):
        client = DocumentClient()
        return client

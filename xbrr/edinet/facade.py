from xbrr.edinet.client.document_list_client import MetaDataClient
from xbrr.edinet.client.document_list_client import DocumentListClient
from xbrr.edinet.client.document_client import DocumentClient
from xbrr.edinet.reader.reader import Reader
from xbrr.edinet.reader.aspects.business import Business
from xbrr.edinet.reader.aspects.company import Company
from xbrr.edinet.reader.aspects.finance import Finance
from xbrr.edinet.reader.aspects.information import Information
from xbrr.edinet.reader.aspects.metadata import Metadata


class APIFacade():

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


class ReaderFacade():

    def read(self, path):
        return Reader(path)


class AspectFacade():

    @property
    def Business(self):
        return Business

    @property
    def Company(self):
        return Company

    @property
    def Finance(self):
        return Finance

    @property
    def Information(self):
        return Information

    @property
    def Metadata(self):
        return Metadata

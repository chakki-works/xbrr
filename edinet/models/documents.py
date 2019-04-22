from edinet.models.metadata import MetaData
from edinet.models.document import Document


class Documents():
    """Document lists"""

    def __init__(self, metadata: MetaData = None, documents: list = ()):
        """
        Keyword Arguments:
            count {MetaData} -- Metadata (default: {None}).
            documents {list} -- Document list (default: {()}).
        """
        self.metadata = metadata
        self.__documents = documents

    @property
    def list(self):
        return self.__documents

    @classmethod
    def create(cls, body: dict) -> "Documents":
        """Create instance from EDINET response.

        Arguments:
            body {dict} -- EDINET response.

        Returns:
            Documents -- Documents and its metadata.
        """
        metadata = MetaData.create(body)
        _documents = body["results"]
        documents = [Document.create(d) for d in _documents]

        instance = cls(metadata, documents)
        return instance

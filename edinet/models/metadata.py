class MetaData():
    """Metadata of document list"""

    def __init__(self, count=-1):
        """Metadata of document list

        Keyword Arguments:
            count {int} -- Number of documents (default: {-1}).
        """
        self.count = count

    @classmethod
    def create(cls, body: dict) -> "MetaData":
        """Create instance from EDINET response.

        Arguments:
            body {dict} -- EDINET response.

        Returns:
            MetaData -- Metadata of document list.
        """
        count = body["metadata"]["resultset"]["count"]
        instance = cls(count=count)
        return instance

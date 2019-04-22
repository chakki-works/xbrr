from typing import Union
from datetime import datetime
import requests
from edinet.client.base_client import BaseClient
from edinet.models import MetaData, Documents


class BaseDocumentListClient(BaseClient):
    """Base client to handle Document List API."""

    def __init__(self, response_type: str):
        """
        Arguments:
            response_type {str} -- Response type of document list api.
        """
        super().__init__(target="documents.json")
        self.response_type = response_type

    def _get(self, date: Union[str, datetime]) -> dict:
        """Get Document List API response.

        Arguments:
            date {(str, datetime)} -- Request date.

        Raises:
            Exception: Date format exception.

        Returns:
            dict -- EDINET Response (JSON).
        """
        url = self.endpoint
        _date = date
        if isinstance(date, str):
            try:
                _date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise Exception("Date format should be yyyy-mm-dd.")

        _date = _date.strftime("%Y-%m-%d")

        params = {
            "date": _date,
            "type": self.response_type
        }

        r = requests.get(url, params=params, verify=False)  # Caution

        if not r.ok:
            r.raise_for_status()
        else:
            body = r.json()
            return body


class MetaDataClient(BaseDocumentListClient):
    """Client to get metadata of document list."""

    def __init__(self):
        super().__init__(response_type="1")  # 1 = only metadata.

    def get(self, date: Union[str, datetime]) -> MetaData:
        """Get metadeta response.

        Arguments:
            date {(str, datetime)} -- Request date.

        Returns:
            MetaData -- Metadata of document list.
        """
        body = self._get(date)
        instance = MetaData.create(body)
        return instance


class DocumentListClient(BaseDocumentListClient):
    """Client to get document list."""

    def __init__(self):
        super().__init__(response_type="2")  # 2 = metadata and document list.

    def get(self, date: Union[str, datetime]) -> Documents:
        """Get metadeta response.

        Arguments:
            date {(str, datetime)} -- Request date.

        Returns:
            Documents -- Document list and its metadata.
        """
        body = self._get(date)
        instance = Documents.create(body)
        return instance

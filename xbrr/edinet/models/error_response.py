from requests.exceptions import HTTPError


class ErrorResponse():
    """Error Response."""

    def __init__(self, status: str = "", message: str = ""):
        """
        Keyword Arguments:
            status {str} -- Error Status (default: {""}).
            message {str} -- Error Message (default: {""}).
        """
        self.status = status
        self.message = message

    def raise_for_status(self, response):
        message = f"HTTP Error {self.status}: {self.message}"
        raise HTTPError(message, response=response)

    @classmethod
    def create(cls, body: dict) -> "ErrorResponse":
        """Create instance from EDINET response.

        Arguments:
            body {dict} -- EDINET response.

        Returns:
            ErrorResponse -- Error response.
        """

        metadata = body["metadata"]
        status = metadata["status"]
        message = metadata["message"]

        instance = cls(status, message)
        return instance

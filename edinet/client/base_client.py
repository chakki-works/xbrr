class BaseClient():
    """"Base API Client.

    Manage the URL and version for the all client.
    """
    BASE_URL = "https://disclosure.edinet-fsa.go.jp/api/{}/{}"

    def __init__(self, target: str, version: str = "v1"):
        """
        Arguments:
            target -- API destination (set by subclass).

        Keyword Arguments:
            version {str} -- API version. (default: {"v1"}).
        """
        self.version = version
        self.target = target

    @property
    def endpoint(self):
        return self.BASE_URL.format(self.version, self.target)

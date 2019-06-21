import importlib
from edinet.client.document_list_client import MetaDataClient
from edinet.client.document_list_client import DocumentListClient
from edinet.client.document_client import DocumentClient
from edinet.parser.xbrl_file import XBRLFile


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


class ParserFacade():

    @classmethod
    def parse(cls, xbrl_path, aspect, feature):
        xbrl_file = XBRLFile(xbrl_path)
        imports = (
            "edinet",
            "parser",
            "aspects",
            aspect
        )

        _class = None
        try:
            module = importlib.import_module(".".join(imports))

            def to_camel(snake_str):
                components = snake_str.split("_")
                return "".join(x.title() for x in components)

            _class_name = to_camel(aspect)
            _class = getattr(module, _class_name)

        except Exception as ex:
            raise Exception(f"Can't load class that matches {aspect} \n {ex}.")

        instance = _class(xbrl_file)
        feature = instance.get(feature)

        return feature

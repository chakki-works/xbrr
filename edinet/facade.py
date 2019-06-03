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
    def parse(cls, xbrl_path, element_name, feature_name, metadata=()):
        xbrl_file = XBRLFile(xbrl_path)
        imports = (
            "edinet",
            "parser",
            "element",
            element_name
        )

        _class = None
        try:
            module = importlib.import_module(".".join(imports))

            def to_camel(snake_str):
                components = snake_str.split("_")
                return "".join(x.title() for x in components)

            _class_name = to_camel(element_name)
            _class = getattr(module, _class_name)

        except Exception as ex:
            raise Exception(f"Can't load class that matches {element_name} \n {ex}.")

        instance = _class(xbrl_file)
        feature = instance.get(feature_name)

        _data = {}
        if len(metadata) > 0:
            _data = metadata

        for k in feature:
            _data[k] = feature[k]

        return _data

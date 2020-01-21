import importlib


class BaseReader():
    """
    Document to Element
    """

    def __init__(self, package):
        self.package = package

    def link_to_path(self, link):
        raise NotImplementedError("You have to implement link_to_path method.")

    def extract(self, aspect_cls_or_str, property=""):
        if not isinstance(aspect_cls_or_str, str):
            aspect_cls = aspect_cls_or_str
            return aspect_cls(self)

        aspect_str = aspect_cls_or_str
        imports = (
            "xbrr",
            self.package,
            "reader",
            "aspects",
            aspect_str
        )

        _class = None
        try:
            module = importlib.import_module(".".join(imports))

            def to_camel(snake_str):
                components = snake_str.split("_")
                return "".join(x.title() for x in components)

            _class_name = to_camel(aspect_str)
            _class = getattr(module, _class_name)

        except Exception as ex:
            raise Exception(f"Can't load class that matches {aspect_str} \n {ex}.")

        aspect = _class(self)
        feature = getattr(aspect, property)

        return feature

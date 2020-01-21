import re
import unicodedata


class BaseParser():
    """
    Element to Value
    """

    def __init__(self, reader, value_class, tags=()):
        self.reader = reader
        self.value_class = value_class
        self.tags = {}
        if len(tags) > 0:
            self.tags = tags
        self._cache = {}

    def normalize(self, text):
        if text is None:
            return ""
        _text = text.strip()
        _text = unicodedata.normalize("NFKC", _text)
        return _text

    def read(self, name):
        if name not in self._cache:
            tag = self.tags[name]
            element = self.reader.find(tag)
            if element:
                self._cache[name] = element
            else:
                without_ns = tag.split(":")[1]  # without ns
                element = self.reader.find(without_ns)
                self._cache[name] = element

        return self._cache[name]

    def get_text_value(self, name):
        element = self.read(name)
        if element:
            value = self.value_class.create_from_element(
                        self.reader, element)

            html = element.html
            if html:
                value.value = html.text
            else:
                value.value = ""

            return value
        else:
            return self.value_class(self.tags[name])

    def search(self, name, pattern):
        element = self.read(name)
        ptn = re.compile(pattern)
        tags = element.html.find_all(["p", "span"])
        text = ""
        if tags and len(tags) > 0:
            for e in tags:
                _text = self.normalize(e.text)
                match = re.search(ptn, _text)
                if match:
                    text = _text
                    break

        return text

    def extract_value(self, name, prefix="", suffix="",
                      filter_pattern=None):
        element = self.read(name)
        text = element.html.text
        if filter_pattern is not None:
            text = self.search(name, filter_pattern)

        pattern = re.compile(f"({prefix}).+?({suffix})")
        match = re.search(pattern, text)
        value = ""

        if match:
            matched = match[0]
            value = matched.replace(prefix, "").replace(suffix, "")
            value = value.strip()
            if value.isdigit():
                value = int(value)
            elif value.replace(".", "").replace("．", "").isdigit():
                value = float(value)

        return value

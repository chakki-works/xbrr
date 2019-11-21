import re
import unicodedata


class XBRLParser():

    def __init__(self, element=None):
        self.element = element

    def normalize(self, text):
        if text is None:
            return ""
        _text = text.strip()
        _text = unicodedata.normalize("NFKC", _text)
        return _text

    def search(self, pattern, element=None):
        html = element if element else self.element.html
        ptn = re.compile(pattern)
        tags = html.find_all(["p", "span"])
        text = ""
        if tags and len(tags) > 0:
            for e in tags:
                _text = self.normalize(e.text)
                match = re.search(ptn, _text)
                if match:
                    text = _text
                    break

        return text

    def extract_value(self, prefix="", suffix="",
                      filter_pattern=None, element=None):

        if filter_pattern is not None:
            text = self.search(filter_pattern, element)
        elif element:
            text = element.text
        else:
            text = self.element.html.text

        text = self.normalize(text)
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

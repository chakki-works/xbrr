import re
import unicodedata


class ContextMatcher():

    def match(self, element):
        raise NotImplementedError("You have to implement match method.")


class TextContextMatcher():

    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def search(self, element):
        tags = element.find_all(["p", "span"])
        text = ""
        if tags and len(tags) > 0:
            for e in tags:
                _text = e.text.strip()
                match = re.search(self.pattern, _text)
                if match:
                    text = _text
                    break

        return text


class ValueExtractor():

    def extract(self, string):
        raise NotImplementedError("You have to implement extract method.")


class TextValueExtractor():

    def __init__(self, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix

    @property
    def pattern(self):
        return f"({self.prefix}).+?({self.suffix})"

    def extract(self, text):
        match = re.search(self.pattern, text)
        value = ""

        if match:
            matched = match[0]
            value = matched.replace(self.prefix, "").replace(self.suffix, "")
            value = value.strip()
            value = unicodedata.normalize("NFKC", value)
            if value.isdigit():
                value = int(value)
            elif value.replace(".", "").replace("．", "").isdigit():
                value = float(value)

        return value

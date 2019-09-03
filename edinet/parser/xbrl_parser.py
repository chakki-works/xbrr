import re
import unicodedata
from edinet.parser.xbrl_file import XBRLElement
from edinet.parser.xbrl_feature import XBRLFeature


class XBRLParser():

    def __init__(self, element=None):
        self._element = element

    def select_element(self, element=None):
        return element if element is not None else self._element

    def normalize(self, text):
        if text is None:
            return ""
        _text = text.strip()
        _text = unicodedata.normalize("NFKC", _text)
        return _text

    def search_text(self, pattern, element=None):
        _element = self.select_element(element)
        ptn = re.compile(pattern)
        tags = _element.find_all(["p", "span"])
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
            text = self.search_text(filter_pattern, element)
        else:
            _element = self.select_element(element)
            text = _element.text

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

    def get_document_feature(self, tag):
        html = XBRLElement(self._element).find(self.TAGS[tag])
        if html._element:
            html = html.to_html()
            raw = html._element.prettify()
            value = self.normalize(html.text)
            feature = XBRLFeature.document(value=value, ground=raw)
        else:
            feature = XBRLFeature.document(value="", ground="")

        return feature

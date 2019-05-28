import re


class XBRLElementReader():

    def __init__(self, element):
        self.element = element

    def find_text(self, pattern):
        tags = self.element.find_all(["p", "span"], string=pattern)
        text = ""
        if tags and len(tags) > 0:
            for e in tags:
                _text = e.text.strip()
                match = re.search(pattern, _text)
                if match:
                    text = _text
                    break

        return text

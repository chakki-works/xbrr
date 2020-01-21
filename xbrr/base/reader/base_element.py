import os
from bs4 import BeautifulSoup


class BaseElement():

    def __init__(self, name, element, reference, reader):
        self.name = name
        self.element = element
        self.reference = reference
        self.reader = reader

    @property
    def reference_path(self):
        names = self.reference.split("#")
        if len(names) > 0:
            return self.reader.link_to_path(names[0])
        else:
            return ""

    @property
    def reference_name(self):
        names = self.reference.split("#")
        if len(names) > 1:
            return names[-1]
        else:
            return ""

    @property
    def exists(self):
        return True if self.element is not None else False

    @property
    def text(self):
        if self.exists:
            return self.element.text
        else:
            return ""

    @property
    def html(self):
        _text = self.text.strip()
        html_text = _text.replace("&lt;", "<").replace("&gt;", ">")
        html = BeautifulSoup(html_text, "html.parser")
        return html

    def _find_file(self, dir, extention):
        path = ""
        for f in os.listdir(dir):
            if f.endswith(extention):
                path = os.path.join(dir, f)
        return path

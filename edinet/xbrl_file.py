import os
import shutil
from bs4 import BeautifulSoup


class XBRLDir():

    def __init__(self, path):
        self.path = path
        self._document_folder = os.path.join(path, "XBRL/PublicDoc")

    def delete(self):
        shutil.rmtree(self.path)

    def _find_file(self, kind, as_xml=True):
        path = ""
        hit = False
        for f in os.listdir(self._document_folder):
            path = os.path.join(self._document_folder, f)
            if not os.path.isfile(path):
                continue
            if kind == "xbrl" and path.endswith(".xbrl"):
                hit = True
            elif kind == "xsd" and path.endswith(".xsd"):
                hit = True
            elif kind == "cal" and path.endswith("_cal.xml"):
                hit = True
            elif kind == "def" and path.endswith("_def.xml"):
                hit = True
            elif kind == "lab" and path.endswith("_lab.xml"):
                hit = True
            elif kind == "lab-en" and path.endswith("_lab-en.xml"):
                hit = True
            elif kind == "pre" and path.endswith("_pre.xml"):
                hit = True
            elif kind == "man" and f.startswith("manifest_") and f.endswith(".xml"):
                hit = True

            if hit:
                break

        if hit:
            if as_xml:
                xml = None
                with open(path, encoding="utf-8-sig") as f:
                    xml = BeautifulSoup(f, "lxml-xml")
                return xml
            else:
                return path
        else:
            return None

    @property
    def xbrl(self):
        return XBRLFile(self._find_file("xbrl", as_xml=False))

    @property
    def xsd(self):
        return self._find_file("xsd")        

    @property
    def cal(self):
        return self._find_file("cal")

    @property
    def def_(self):
        return self._find_file("def")

    @property
    def lab(self):
        return self._find_file("lab")

    @property
    def lab_en(self):
        return self._find_file("lab-en")

    @property
    def pre(self):
        return self._find_file("pre")

    @property
    def man(self):
        return self._find_file("man")


class XBRLFile():

    def __init__(self, path):
        self.path = path
        self._root = None

        # Load XBRL file
        if not os.path.exists(self.path):
            raise FileNotFoundError()

        with open(self.path, encoding="utf-8-sig") as f:
            self._root = BeautifulSoup(f, "lxml-xml")

    @property
    def root(self):
        return self._root

    @property
    def text(self):
        return self._root.text

    def find(self, tag, attrs={}, recursive=True, text=None,
             **kwargs):
        tag_element = self._root.find(tag, attrs, recursive, text, **kwargs)
        return XBRLElement(tag_element)

    def find_all(self, tag, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
        tag_elements = self._root.find_all(
                        tag, attrs, recursive, text, limit, **kwargs)

        return [XBRLElement(e) for e in tag_elements]

    def parse_by(self, parser_cls):
        return parser_cls(self._root)


class XBRLElement():

    def __init__(self, element):
        self._element = element

    @property
    def element(self):
        return self._element

    @property
    def text(self):
        return self._element.text

    def get(self, attribute):
        return self._element[attribute]

    def find(self, tag, attrs={}, recursive=True, text=None,
             **kwargs):
        tag_element = self._element.find(
                        tag, attrs, recursive, text, **kwargs)
        return XBRLElement(tag_element)

    def find_all(self, tag, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
        tag_elements = self._element.find_all(
                        tag, attrs, recursive, text, limit, **kwargs)

        return [XBRLElement(e) for e in tag_elements]

    def to_html(self):
        _text = self._element.text.strip()
        html_text = _text.replace("&lt;", "<").replace("&gt;", ">")
        html = BeautifulSoup(html_text, "html.parser")
        return XBRLElement(html)

    def parse_by(self, parser_cls):
        return parser_cls(self._element)

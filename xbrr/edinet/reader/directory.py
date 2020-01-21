import os
import shutil
from bs4 import BeautifulSoup


class Directory():

    def __init__(self, root):
        self.root = root
        self._document_folder = os.path.join(root, "XBRL/PublicDoc")
        self._cache = {}

    def delete(self):
        shutil.rmtree(self.root)

    def _find_file(self, kind, as_xml=True):
        path = ""
        hit = False
        for f in os.listdir(self._document_folder):
            path = os.path.join(self._document_folder, f)
            if not os.path.isfile(path):
                path = ""
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
                if path in self._cache:
                    xml = self._cache[path]
                else:
                    with open(path, encoding="utf-8-sig") as f:
                        xml = BeautifulSoup(f, "lxml-xml")
                return xml
            else:
                return path
        else:
            return None

    @property
    def xbrl(self):
        return self._find_file("xbrl")

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

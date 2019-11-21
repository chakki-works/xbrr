import os
from bs4 import BeautifulSoup
from edinet.parser.xbrl_parser import XBRLParser


class XBRLElement():

    def __init__(self, name, element, location, reader):
        self.name = name
        self.element = element
        self.location = location
        self.reader = reader

    @property
    def text(self):
        return self.element.text

    @property
    def html(self):
        _text = self.element.text.strip()
        html_text = _text.replace("&lt;", "<").replace("&gt;", ">")
        html = BeautifulSoup(html_text, "html.parser")
        return html

    @property
    def content(self):
        return XBRLParser(self)

    def _location_to_path_element(self, kind, location=""):
        r = self.reader
        element = ""
        path = location if location else self.location
        if "#" in path:
            path, element = path.split("#")

        if r.taxonomy and \
           path.startswith(r.taxonomy.prefix):
            path = path.replace(r.taxonomy.prefix, "")
            path = os.path.join(r.taxonomy.root, path)

        else:
            path = os.path.join(r.root._document_folder, path)

        return path, element

    def _find_file(self, dir, extention):
        path = ""
        for f in os.listdir(dir):
            if f.endswith(extention):
                path = os.path.join(dir, f)
        return path

    @property
    def xsd(self):
        path, element = self._location_to_path_element()
        xml = None
        if path.endswith(".xsd"):
            xml = self.reader._read_from_cache(path)
        else:
            _dir = os.path.dirname(path)
            path = self._find_file(_dir, ".xsd")
            xml = self.reader._read_from_cache(path)

        element = xml.find("xsd:element", {"id": element})
        return element

    def _get_label(self, extention, verbose):
        path, element = self._location_to_path_element()
        xml = None
        _dir = os.path.join(os.path.dirname(path), "label")
        label_path = self._find_file(_dir, extention)
        xml = self.reader._read_from_cache(label_path)
        href = f"../{os.path.basename(path)}#{element}"
        targets = self._read_link(
            xml=xml, arc_name="link:labelArc", location=href,
            target_name="link:label", target_attribute="id")

        if len(targets) > 1:
            for lb in targets:
                if lb["xlink:role"].endswith("verboseLabel") and verbose:
                    label = lb
                    break
                else:
                    label = lb

        elif len(targets) > 0:
            label = targets[0]

        return label

    def lab(self, verbose=False):
        return self._get_label("_lab.xml", verbose)

    def lab_en(self, verbose=False):
        return self._get_label("_lab_en.xml", verbose)

    def lab_gla(self, verbose=False):
        return self._get_label("_lab_gla.xml", verbose)

    def _read_link(self, xml, arc_name, location="",
                   target_name="", target_attribute=""):

        # link: href: absolute path to element definition by url format.
        # name: underscore separated name. when used by tag, it is splited by ":"
        # name is solved by namespace so
        # name => link is good approach.

        location = location if location else self.location
        label = xml.find("link:loc", {"xlink:href": location})
        arc = None

        if label is not None:
            arc = xml.find(arc_name, {"xlink:from": label["xlink:label"]})
        else:
            arc = xml.find(arc_name, {"xlink:label": self.name})

        if arc is None:
            return []

        target_name = target_name if target_name else "link:loc"
        target_attribute = target_attribute if target_attribute else "xlink:label"
        targets = []
        if arc is not None:
            targets = xml.find_all(target_name, {target_attribute: arc["xlink:to"]})

        return targets

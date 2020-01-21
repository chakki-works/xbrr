import os
from xbrr.base.reader.base_element import BaseElement


class Element(BaseElement):

    def __init__(self, name, element, reference, reader):
        super().__init__(name, element, reference, reader)
        self.name = name
        self.element = element
        self.reference = reference
        self.reader = reader

    @property
    def xsd(self):
        name = self.reference_name
        path = self.reference_path
        xml = None

        if path.endswith(".xsd"):
            xml = self.reader._read_from_cache(path)
        else:
            path = self._find_file(os.path.dirname(path), ".xsd")

        if os.path.dirname(path).endswith("PublicDoc"):
            element = xml.find("element", {"id": name})
        else:
            element = xml.find("xsd:element", {"id": name})

        return element

    def label(self, kind="lab", verbose=False):
        label = ""
        if kind == "en":
            label = self._get_label("_lab_en.xml", verbose)
        elif kind == "gla":
            label = self._get_label("_lab_gla.xml", verbose)
        else:
            label = self._get_label("_lab.xml", verbose)

        if isinstance(label, str):
            return label
        else:
            return label.text

    def _get_label(self, extention, verbose):
        name = self.reference_name
        path = self.reference_path
        xml = None

        if os.path.dirname(path).endswith("PublicDoc"):
            label_path = self._find_file(os.path.dirname(path), extention)
            href = self.reference
        else:
            _dir = os.path.join(os.path.dirname(path), "label")
            label_path = self._find_file(_dir, extention)
            href = f"../{os.path.basename(path)}#{name}"

        xml = self.reader._read_from_cache(label_path)

        targets = self._read_link(
            xml=xml, arc_name="link:labelArc", reference=href,
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
        else:
            label = None

        return label

    def _read_link(self, xml, arc_name, reference="",
                   target_name="", target_attribute=""):

        # link: href: absolute path to element definition by url format.
        # name: underscore separated name. when used by tag, it is splited by ":"
        # name is solved by namespace so
        # name => link is good approach.

        reference = reference if reference else self.reference
        label = xml.find("link:loc", {"xlink:href": reference})
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
            if len(targets) == 0 and target_attribute != "xlink:label":
                targets = xml.find_all(target_name, {"xlink:label": arc["xlink:to"]})

        return targets

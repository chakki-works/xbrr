import os
from bs4 import BeautifulSoup
import pandas as pd
from edinet.document.xbrl_dir import XBRLDir
from edinet.document.xbrl_element import XBRLElement
from edinet.document.taxonomy import Taxonomy


class XBRLReader():

    def __init__(self, xbrl_file="", xbrl_dir="", taxonomy=""):
        if not xbrl_file and not xbrl_dir:
            raise Exception("You have to specify xbrl_file or xbrl_dir")

        self.xbrl_file = xbrl_file
        self.xbrl_dir = XBRLDir(xbrl_dir)
        self.taxonomy = Taxonomy(taxonomy)
        self._cache = {}

    def _read_from_cache(self, path):
        xml = None
        if path in self._cache:
            xml = self._cache[path]
        else:
            with open(path, encoding="utf-8-sig") as f:
                xml = BeautifulSoup(f, "lxml-xml")
            self._cache[path] = xml
        return self._cache[path]

    @property
    def roles(self):
        role_ref_tags = self.xbrl.find_all("link:roleRef")
        role_ref_elements = [t.element for t in role_ref_tags]
        roles = {}
        for e in role_ref_elements:
            link = e["xlink:href"]
            roles[e["roleURI"]] = {
                "link": e["xlink:href"],
                "name": self.read_by_link(link).element.find("link:definition").text
            }

        return roles

    @property
    def namespaces(self):
        schema = self.xbrl.find("xbrli:xbrl")
        namespaces = {}
        for a in schema.element.attrs:
            if a.startswith("xmlns:"):
                namespaces[a.replace("xmlns:", "")] = schema.element.attrs[a]

        return namespaces

    @property
    def xbrl(self):
        if self.xbrl_dir.root:
            path = self.xbrl_dir.xbrl._find_file("xbrl", as_xml=False)
        else:
            path = self.xbrl_file
        return self._read_from_cache(path)

    def read_by_link(self, link):
        if not self.xbrl_dir.root or not self.taxonomy.root:
            raise Exception("XBRL directory or taxonomy is required.")

        path = link
        element = ""

        if "#" in path:
            path, element = path.split("#")

        if self.taxonomy and path.startswith(self.taxonomy.prefix):
            path = path.replace(self.taxonomy.prefix, "")
            path = os.path.join(self.taxonomy.root, path)
        else:
            path = os.path.join(self.root._document_folder, path)

        xml = self._read_from_cache(path)

        if element:
            xml = xml.select(f"#{element}")
            if len(xml) > 0:
                xml = xml[0]
            xml = XBRLElement(element, xml, link, self)

        return xml

    def read_role(self, role_link):
        pre = self.xbrl_dir.pre.find(
            "link:presentationLink", {"xlink:role": role_link})

        nodes = {}
        for i, arc in enumerate(pre.find_all("link:presentationArc")):
            if not arc["xlink:arcrole"].endswith("parent-child"):
                print("Unexpected arctype.")
                continue

            parent = Node(pre.find("link:loc",
                                   {"xlink:label": arc["xlink:from"]}), i)
            child = Node(pre.find("link:loc", {"xlink:label": arc["xlink:to"]}),
                         arc["order"])

            if child.name not in nodes:
                nodes[child.name] = child
            else:
                nodes[child.name].order = arc["order"]

            if parent.name not in nodes:
                nodes[parent.name] = parent

            nodes[child.name].add_parent(nodes[parent.name])

        parent_depth = -1
        for name in nodes:
            if parent_depth < nodes[name].depth:
                parent_depth = nodes[name].depth

        data = []
        for name in nodes:
            n = nodes[name]
            item = {}
            parents = n.get_parents()
            parents = parents + ([""] * (parent_depth - len(parents)))

            for i, p in enumerate(parents):
                name = p if isinstance(p, str) else p.name
                order = "0" if isinstance(p, str) else p.order
                item[f"parent_{i}"] = name
                item[f"parent_{i}_order"] = order

            item["element"] = n.name
            item["order"] = n.order
            item["depth"] = n.depth

            # Label
            item["label"] = self.read_by_link(n.location).label().text

            # Definition
            _def = self.read(n.location).definition()
            item["abstract"] = _def["abstract"]
            item["type"] = _def["type"]

            if "xbrli:periodType" in _def.attrs:
                item["period_type"] = _def["xbrli:periodType"]

            if "xbrli:balance" in _def.attrs:
                item["balance"] = _def["xbrli:balance"]

            data.append(item)

        role_data = pd.DataFrame(data)
        role_data.sort_values(by=[c for c in data.columns
                                  if c.endswith("order")],
                              inplace=True)

        return role_data

    def read_by_role(self, role_link):
        role_data = self.read_role(role_link)
        parent_columns = [c for c in role_data.columns
                          if c.startswith("parent") and c.endswith("order")]
        parent_depth = len(parent_columns)
        xbrl_data = []

        for i, row in role_data.iterrows():
            tag_name = row["element"]

            for n in self.namespaces:
                if tag_name.startswith(n):
                    tag_name = f"{n}:{tag_name.replace(n + '_', '')}"
                    break

            tag = self.xbrl.find(tag_name)
            element = tag.element
            if element is None:
                continue

            item = {}
            for k in role_data.columns:
                item[k] = row[k]

            for i in range(parent_depth):
                mask = role_data["element"] == row[f"parent_{i}"]
                parent_label = role_data[mask]["label"].tolist()
                if len(parent_label) > 0:
                    parent_label = parent_label[0]
                else:
                    parent_label = ""
                item[f"parent_{i}_label"] = parent_label

            item["value"] = element.text

            context_id = element["contextRef"]
            if context_id.endswith("NonConsolidatedMember"):
                item["individual"] = True
            else:
                item["individual"] = False

            context = self.xbrl.find("xbrli:context", {"id": context_id})
            if item["period_type"] == "duration":
                item["period"] = context.find("xbrli:endDate").text
                item["period_begin"] = context.find("xbrli:startDate").text
            else:
                item["period"] = context.find("xbrli:instant").text
                item["period_begin"] = None

            if "unitRef" in element.attrs:
                item["unit"] = element["unitRef"]
            else:
                item["unit"] = ""

            xbrl_data.append(item)

        xbrl_data = pd.DataFrame(xbrl_data)
        return xbrl_data

    def extract(self, aspect_cls):
        return aspect_cls(self)

    def find(self, tag, attrs={}, recursive=True, text=None,
             **kwargs):
        tag_element = self.xbrl.find(tag, attrs, recursive, text, **kwargs)
        return self._to_element(tag_element)

    def find_all(self, tag, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
        tag_elements = self.xbrl.find_all(
                        tag, attrs, recursive, text, limit, **kwargs)

        return [self._to_element(e) for e in tag_elements]

    def _to_element(self, tag):
        if tag is None:
            return None
        location = f"{tag.namespace}#{tag.name}"
        return XBRLElement(tag, tag, location, self)


class Node():

    def __init__(self, element, order=0):
        self.element = element
        self.parent = None
        self.order = order

    def add_parent(self, parent):
        self.parent = parent

    @property
    def name(self):
        return self.element["xlink:href"].split("#")[-1]

    @property
    def label(self):
        return self.element["xlink:label"]

    @property
    def location(self):
        return self.element["xlink:href"]

    @property
    def depth(self):
        return len(self.get_parents())

    @property
    def path(self):
        parents = list(reversed(self.get_parents()))
        if len(parents) == 0:
            return self.name
        else:
            path = str(self.order) + " " + self.name
            for p in parents:
                path = p.name + "/" + path
            return path

    def get_parents(self):
        parents = []
        if self.parent is None:
            return parents
        else:
            p = self.parent
            while p is not None:
                parents.insert(0, p)
                p = p.parent
            return parents

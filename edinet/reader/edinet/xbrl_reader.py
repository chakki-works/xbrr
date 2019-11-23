import os
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from edinet.reader.edinet.xbrl_dir import XBRLDir
from edinet.reader.edinet.taxonomy import Taxonomy
from edinet.reader.edinet.edinet_value import EDINETValue, EDINETElementSchema
from edinet.reader.edinet.edinet_element import EDINETElement
from edinet.reader.base_reader import BaseReader


class XBRLReader(BaseReader):

    def __init__(self, xbrl_dir_or_file="", taxonomy=None):
        super().__init__()
        self._taxonomy_kind = "edinet"
        self._cache = {}

        if os.path.isdir(xbrl_dir_or_file):
            self.xbrl_dir = XBRLDir(xbrl_dir_or_file)
            self.xbrl_file = self.xbrl_dir._find_file("xbrl", as_xml=False)
        elif os.path.isfile(xbrl_dir_or_file):
            self.xbrl_file = xbrl_dir_or_file
            self.xbrl_dir = None
        else:
            raise Exception(
                f"File or directory {xbrl_dir_or_file} does not Exsit.")

        if isinstance(taxonomy, Taxonomy):
            self.taxonomy = taxonomy
        else:
            if self.xbrl_dir:
                root = Path(self.xbrl_dir.root).parent
            else:
                root = Path(self.xbrl_file).parent

            if root.name == "raw":
                # Cookiecutter data science structure
                root = root.parent
            root = root.joinpath("external")
            self.taxonomy = Taxonomy(root)
        self.taxonomy_year = -1
        self.__set_taxonomy_year()

    def __set_taxonomy_year(self):
        date = self.xbrl.find("jpdei_cor:CurrentFiscalYearEndDateDEI").text
        date = datetime.strptime(date, "%Y-%m-%d")
        for y in sorted(list(self.taxonomy.EDINET_TAXONOMY.keys()), reverse=True):
            boarder_date = datetime(y, 3, 31)
            if date > boarder_date:
                self.taxonomy_year = y
                break

    @property
    def roles(self):
        role_refs = self.find_all("link:roleRef")
        roles = {}
        for e in role_refs:
            element = e.element
            link = element["xlink:href"]
            roles[element["roleURI"]] = {
                "link": element["xlink:href"],
                "name": self.read_by_link(link).element.find("link:definition").text
            }

        return roles

    @property
    def taxonomy_path(self):
        return self.taxonomy.root.joinpath("taxonomy", str(self.taxonomy_year))

    @property
    def namespaces(self):
        schema = self.xbrl.find("xbrli:xbrl")
        namespaces = {}
        for a in schema.attrs:
            if a.startswith("xmlns:"):
                namespaces[a.replace("xmlns:", "")] = schema.attrs[a]

        return namespaces

    @property
    def xbrl(self):
        if self.xbrl_dir:
            path = self.xbrl_dir._find_file("xbrl", as_xml=False)
        else:
            path = self.xbrl_file
        return self._read_from_cache(path)

    def _read_from_cache(self, path):
        xml = None
        if path in self._cache:
            xml = self._cache[path]
        else:
            with open(path, encoding="utf-8-sig") as f:
                xml = BeautifulSoup(f, "lxml-xml")
            self._cache[path] = xml
        return self._cache[path]

    def link_to_path(self, link):
        path = link
        if self.taxonomy and path.startswith(self.taxonomy.prefix):
            path = link.replace(self.taxonomy.prefix, "")
            path = os.path.join(self.taxonomy_path, path)
            if not os.path.exists(path):
                _path = Path(path)
                xbrl_date = _path.parent.name
                # check namespace directory
                taxonomy_date = ""
                if _path.parent.parent.exists():
                    for d in _path.parent.parent.iterdir():
                        if d.is_dir():
                            taxonomy_date = d.name
                            break

                if taxonomy_date and taxonomy_date != xbrl_date:
                    path = path.replace(xbrl_date, taxonomy_date)
        else:
            path = os.path.join(self.xbrl_dir._document_folder, path)

        return path

    def read_by_link(self, link):
        if link.startswith(self.taxonomy.prefix):
            self.taxonomy.download(self.taxonomy_year)

        path = link
        element = ""

        if "#" in path:
            path, element = path.split("#")

        path = self.link_to_path(path)
        xml = self._read_from_cache(path)

        if element:
            xml = xml.select(f"#{element}")
            if len(xml) > 0:
                xml = xml[0]
            xml = EDINETElement(element, xml, link, self)

        return xml

    def read_schema_by_role(self, role_link):
        if self.xbrl_dir is None:
            raise Exception("XBRL directory is required.")

        pre = self.xbrl_dir.pre.find(
            "link:presentationLink", {"xlink:role": role_link})

        def get_name(loc):
            return loc["xlink:href"].split("#")[-1]
        create = EDINETElementSchema.create_from_reference

        nodes = {}
        for i, arc in enumerate(pre.find_all("link:presentationArc")):
            if not arc["xlink:arcrole"].endswith("parent-child"):
                print("Unexpected arctype.")
                continue

            parent = pre.find("link:loc", {"xlink:label": arc["xlink:from"]})
            child = pre.find("link:loc", {"xlink:label": arc["xlink:to"]})

            if get_name(child) not in nodes:
                c = create(self, child["xlink:href"]).set_alias(child["xlink:label"])
                nodes[get_name(child)] = Node(c, arc["order"])
            else:
                nodes[get_name(child)].order = arc["order"]

            if get_name(parent) not in nodes:
                p = create(self, parent["xlink:href"]).set_alias(parent["xlink:label"])
                nodes[get_name(parent)] = Node(p, i)

            nodes[get_name(child)].add_parent(nodes[get_name(parent)])

        parent_depth = -1
        for name in nodes:
            if parent_depth < nodes[name].depth:
                parent_depth = nodes[name].depth

        schemas = []
        for name in nodes:
            n = nodes[name]
            item = {}
            parents = n.get_parents()
            parents = parents + ([""] * (parent_depth - len(parents)))

            for i, p in enumerate(parents):
                name = p if isinstance(p, str) else p.name
                order = "0" if isinstance(p, str) else p.order
                item[f"parent_{i}"] = name
                item[f"parent_{i}_label"] = ""
                item[f"parent_{i}_order"] = order

            item["order"] = n.order
            item["depth"] = n.depth
            item.update(n.element.to_dict())
            schemas.append(item)

        schemas = pd.DataFrame(schemas)
        schemas.sort_values(by=[c for c in schemas.columns
                                if c.endswith("order")],
                            inplace=True)

        label_dict = pd.Series(schemas["name"],
                               index=schemas["label"]).to_dict()

        for i, row in schemas.iterrows():
            for i in range(parent_depth):
                name = row[f"parent_{i}"]
                if name in label_dict:
                    schemas.at[i, f"parent_{i}_label"] = label_dict[name]

        return schemas

    def read_value_by_role(self, role_link):
        schemas = self.read_role(role_link)

        xbrl_data = []
        for i, row in schemas.iterrows():
            tag_name = row["name"]

            for n in self.namespaces:
                if tag_name.startswith(n):
                    tag_name = f"{n}:{tag_name.replace(n + '_', '')}"
                    break

            tag = self.xbrl.find(tag_name)
            element = tag.element
            if element is None:
                continue

            item = {}
            for k in schemas.columns:
                item[k] = row[k]

            value = EDINETValue(self, element).to_dict()
            for k in value:
                if k not in item:
                    item[k] = value[k]

            xbrl_data.append(item)

        xbrl_data = pd.DataFrame(xbrl_data)
        return xbrl_data

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
        reference = f"{tag.namespace}#{tag.name}"
        return EDINETElement(tag, tag, reference, self)


class Node():

    def __init__(self, element, order=0):
        self.element = element
        self.parent = None
        self.order = order

    def add_parent(self, parent):
        self.parent = parent

    @property
    def name(self):
        return self.element.name

    @property
    def label(self):
        return self.element.label

    @property
    def reference(self):
        return self.element.reference

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

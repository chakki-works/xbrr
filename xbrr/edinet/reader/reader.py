import os
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from joblib import Parallel, delayed
from xbrr.base.reader.base_reader import BaseReader
from xbrr.edinet.reader.directory import Directory
from xbrr.edinet.reader.taxonomy import Taxonomy
from xbrr.edinet.reader.element import Element
from xbrr.edinet.reader.element_value import ElementValue
from xbrr.edinet.reader.element_schema import ElementSchema


class Reader(BaseReader):

    def __init__(self, xbrl_dir_or_file="", taxonomy=None):
        super().__init__("edinet")
        self.__xbrl_dir_or_file = xbrl_dir_or_file
        self._cache = {}

        if os.path.isdir(xbrl_dir_or_file):
            self.xbrl_dir = Directory(xbrl_dir_or_file)
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
        self.taxonomy_year = ""
        self.__set_taxonomy_year()

    def set_cache(self, cache):
        self._cache = cache
        return self

    def __reduce_ex__(self, proto):
        return type(self), (self.__xbrl_dir_or_file, self.taxonomy)

    def __set_taxonomy_year(self):
        self.taxonomy_year = ""
        date = self.xbrl.find("jpdei_cor:CurrentFiscalYearEndDateDEI").text
        kind = self.xbrl.find("jpdei_cor:TypeOfCurrentPeriodDEI").text
        date = datetime.strptime(date, "%Y-%m-%d")
        for y in sorted(list(self.taxonomy.TAXONOMIES.keys()), reverse=True):
            boarder_date = datetime(int(y[:4]), 3, 31)
            if kind[0] in ("Q", "H") and date > boarder_date:
                self.taxonomy_year = y
            elif date >= boarder_date:
                if y == 2019:
                    self.taxonomy_year = "2019_cg_ifrs"
                else:
                    self.taxonomy_year = y

            if self.taxonomy_year:
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
        elif self.xbrl_dir:
            path = self.xbrl_dir._find_file("xsd", as_xml=False)
        else:
            path = os.path.dirname(self.xbrl_file)

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
            # xml = xml.find("element", {"id": element})
            if len(xml) > 0:
                xml = xml[0]
            xml = Element(element, xml, link, self)

        return xml

    def read_schema_by_role(self, role_link, link_type="presentation",
                            label_kind="", label_verbose=False):
        if self.xbrl_dir is None:
            raise Exception("XBRL directory is required.")

        doc = None
        link_node = ""
        arc_node = ""
        if link_type == "presentation":
            doc = self.xbrl_dir.pre
            link_node = "link:presentationLink"
            arc_node = "link:presentationArc"
        elif link_type == "calculation":
            doc = self.xbrl_dir.cal
            link_node = "link:calculationLink"
            arc_node = "link:calculationArc"
        else:
            raise Exception(f"Does not support {link_type}.")

        role = doc.find(link_node, {"xlink:role": role_link})

        def get_name(loc):
            return loc["xlink:href"].split("#")[-1]

        def create(reader, reference):
            return ElementSchema.create_from_reference(
                        reader, reference, label_kind, label_verbose)

        nodes = {}
        arc_role = ""
        if link_type == "calculation":
            arc_role = "summation-item"
        else:
            arc_role = "parent-child"

        locs = {}
        for loc in role.find_all("link:loc"):
            locs[loc["xlink:label"]] = loc

        for i, arc in enumerate(role.find_all(arc_node)):
            if not arc["xlink:arcrole"].endswith(arc_role):
                print("Unexpected arctype.")
                continue

            parent = locs[arc["xlink:from"]]
            child = locs[arc["xlink:to"]]

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

            for i, p in zip(reversed(range(parent_depth)), parents):
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

        label_dict = pd.Series(schemas["label"].tolist(),
                               index=schemas["name"].tolist()).to_dict()

        for i, row in schemas.iterrows():
            for j in range(parent_depth):
                name = row[f"parent_{j}"]
                if name in label_dict:
                    schemas.loc[i, f"parent_{j}_label"] = label_dict[name]

        return schemas

    def read_value_by_role(self, role_link, link_type="presentation",
                           label_kind="", label_verbose=False):
        schemas = self.read_schema_by_role(role_link, link_type,
                                           label_kind, label_verbose)

        targets = []
        xbrl_data = []
        for i, row in schemas.iterrows():
            tag_name = row["name"]

            for n in self.namespaces:
                if tag_name.startswith(n):
                    tag_name = tag_name.replace(f"{n}_", f"{n}:")
                    break

            tag_element = self.xbrl.find(tag_name)
            if tag_element is None:
                continue

            item = {}
            for k in schemas.columns:
                item[k] = row[k]

            targets.append((tag_name, item))

        def read_value(reader, target, label_kind, label_verbose):
            name, item = target
            results = []
            for element in reader.find_all(name):
                value = ElementValue.create_from_element(
                            reader, element, label_kind, label_verbose).to_dict()
                for k in value:
                    if k not in item:
                        item[k] = value[k]

                results.append(item)
            return results

        results = Parallel(n_jobs=-1)(delayed(read_value)(
                                        self, t, label_kind, label_verbose)
                                      for t in targets)

        for r in results:
            if len(r) > 0:
                xbrl_data += r

        xbrl_data = pd.DataFrame(xbrl_data)
        return xbrl_data

    def find(self, tag, attrs={}, recursive=True, text=None,
             **kwargs):
        element = self.xbrl.find(tag, attrs, recursive, text, **kwargs)
        return self._to_element(tag, element)

    def find_all(self, tag, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
        elements = self.xbrl.find_all(
                        tag, attrs, recursive, text, limit, **kwargs)

        return [self._to_element(tag, e) for e in elements]

    def _to_element(self, tag, element):
        if element is None:
            return None

        reference = tag.replace(":", "_")
        if element.namespace:
            path = self.link_to_path(element.namespace)
            namespace_root, prefix = os.path.split(path)
            xsd_name = ""
            if os.path.isdir(namespace_root):
                fs = [f for f in os.listdir(namespace_root)
                      if f.startswith(prefix) and f.endswith(".xsd")]
                if len(fs) > 0:
                    xsd_name = fs[0]

            if element.namespace.startswith(self.taxonomy.prefix):
                namespace_root = namespace_root.replace(
                                    str(self.taxonomy_path) + os.sep,
                                    self.taxonomy.prefix)
            else:
                namespace_root = ""

            if namespace_root:
                reference = f"{namespace_root}/{xsd_name}#{reference}"
            else:
                reference = f"{xsd_name}#{reference}"

        return Element(tag, element, reference, self)


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

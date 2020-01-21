from pathlib import Path
from zipfile import ZipFile
import requests


class Taxonomy():
    TAXONOMIES = {
        "2013": "https://www.fsa.go.jp/search/20130821/editaxonomy2013New.zip",
        "2014": "https://www.fsa.go.jp/search/20140310/1c.zip",
        "2015": "https://www.fsa.go.jp/search/20150310/1c.zip",
        "2016": "https://www.fsa.go.jp/search/20160314/1c.zip",
        "2017": "https://www.fsa.go.jp/search/20170228/1c.zip",
        "2018": "https://www.fsa.go.jp/search/20180228/1c_Taxonomy.zip",
        "2019": "https://www.fsa.go.jp/search/20190228/1c_Taxonomy.zip",
        "2019_cg_ifrs": "https://www.fsa.go.jp/search/20180316/1c_Taxonomy.zip"
    }

    def __init__(self, taxonomy_root):
        self.root = taxonomy_root
        self.prefix = "http://disclosure.edinet-fsa.go.jp/taxonomy/"

    def __reduce_ex__(self, proto):
        return type(self), (self.root,)

    def download(self, year):
        year = str(year)
        expand_dir = self.root.joinpath("taxonomy").joinpath(year)
        taxonomy_file = self.root.joinpath(f"{year}_taxonomy.zip")

        download = False

        if not self.root.exists():
            self.root.mkdir(parents=True, exist_ok=True)
            download = True

        if not expand_dir.exists():
            expand_dir.mkdir(parents=True, exist_ok=True)
            download = True

        if download:
            # Download
            r = requests.get(self.TAXONOMIES[year], stream=True)
            with taxonomy_file.open(mode="wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

            # Extract
            with ZipFile(taxonomy_file, "r") as zip:
                for f in zip.namelist():
                    dirs = Path(f).parts
                    # Avoid Japanese path
                    taxonomy_at = dirs.index("taxonomy") if "taxonomy" in dirs else -1
                    if taxonomy_at > 0 and len(dirs) > (taxonomy_at + 1):
                        dirs = dirs[(dirs.index("taxonomy") + 1):]
                        _to = expand_dir.joinpath("/".join(dirs))
                        info = zip.getinfo(f)
                        if info.is_dir() and not _to.exists():
                            _to.mkdir(parents=True, exist_ok=True)
                        else:
                            _to.parent.mkdir(parents=True, exist_ok=True)
                            with _to.open("wb") as _to_f:
                                _to_f.write(zip.read(f))

            taxonomy_file.unlink()

        return expand_dir

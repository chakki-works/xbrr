from pathlib import Path
from zipfile import ZipFile
import requests


class Taxonomy():
    EDINET_TAXONOMY = {
        2013: "https://www.fsa.go.jp/search/20130821/editaxonomy2013New.zip",
        2014: "https://www.fsa.go.jp/search/20140310/1c.zip",
        2015: "https://www.fsa.go.jp/search/20150310/1c.zip",
        2016: "https://www.fsa.go.jp/search/20160314/1c.zip",
        2017: "https://www.fsa.go.jp/search/20170228/1c.zip",
        2018: "https://www.fsa.go.jp/search/20180228/1c_Taxonomy.zip",
        2019: "https://www.fsa.go.jp/search/20190228/1c_Taxonomy.zip"
    }

    def __init__(self, taxonomy_root):
        self.root = taxonomy_root
        self.prefix = "http://disclosure.edinet-fsa.go.jp/taxonomy/"

    def download(self, year):
        year = int(year)
        expand_dir = self.root.joinpath("taxonomy").joinpath(str(year))
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
            self.root.mkdir(parents=True, exist_ok=True)
            r = requests.get(self.EDINET_TAXONOMY[year], stream=True)
            with taxonomy_file.open(mode="wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

            # Extract
            with ZipFile(taxonomy_file, "r") as zip:
                for f in zip.namelist():
                    # Avoid Japanese path 
                    dirs = f.split("/")
                    if dirs[2] == "taxonomy":
                        _to = expand_dir.joinpath("/".join(dirs[3:]))
                        _to.parent.mkdir(parents=True, exist_ok=True)
                        with _to.open("wb") as _to_f:
                            _to_f.write(zip.read(f))

            taxonomy_file.unlink()

        return expand_dir

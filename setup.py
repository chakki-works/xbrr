from setuptools import setup
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip


pipenv_file = Project(chdir=False).parsed_pipfile
dependencies = convert_deps_to_pip(pipenv_file["packages"], r=False)


setup(
    name="edinet-python",
    version="0.1.0",
    description="EDINET API Client for Python.",
    keywords=["EDINET", "API"],
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    license="MIT",
    packages=[
        "edinet",
        "edinet.client",
        "edinet.models"
        ],
    url="https://github.com/chakki-works/edinet-python",
    install_requires=dependencies,
)

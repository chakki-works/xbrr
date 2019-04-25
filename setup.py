from setuptools import setup


readme = ""
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="edinet-python",
    version="0.1.2",
    description="EDINET API Client for Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
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
    install_requires=[
        "requests>=2.21.0"
    ],
)

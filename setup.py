from setuptools import find_packages, setup


readme = ""
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="xbrr",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="eXtensible Business Report Reader.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["XBRL", "EDINET", "API"],
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    license="MIT",
    packages=find_packages(exclude=('tests',)),
    url="https://github.com/chakki-works/xbrr",
    install_requires=[
        "beautifulsoup4>=4.8.2",
        "joblib>=0.14.1",
        "lxml>=4.4.2",
        "requests>=2.22.0",
        "tqdm>=4.41.1"
    ]
)

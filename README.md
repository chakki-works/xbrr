# edinet-python

[![PyPI version](https://badge.fury.io/py/edinet-python.svg)](https://badge.fury.io/py/edinet-python)
[![Build Status](https://travis-ci.org/chakki-works/edinet-python.svg?branch=master)](https://travis-ci.org/chakki-works/edinet-python)
[![codecov](https://codecov.io/gh/chakki-works/edinet-python/branch/master/graph/badge.svg)](https://codecov.io/gh/chakki-works/edinet-python)

[EDINET API](https://disclosure.edinet-fsa.go.jp/EKW0EZ0015.html) Client for Python.

## How to use

### Document list API

Get document list of specific day.

Only metadata (number of documents).

```py
import edinet


metadata = edinet.api.metadata.get("2019-01-31")
print(f"Number of documents is {metadata.count}")

```

Get document list.

```py
import edinet


documents = edinet.api.documents.get("2019-01-31")
print(f"Number of documents is {len(documents.list)}")
print(f"Title of first document is {documents.list[0].title}")
```

### Document API

Get document file of specific document id.

```py
from pathlib import Path
import edinet


xbrl_path = edinet.api.document.get_xbrl("S100FGR9", save_dir=Path.cwd())
pdf_path = edinet.api.document.get_pdf("S100FGR9", save_dir=Path.cwd())
```

## Install

```
pip install edinet-python
```

# edinet-python

[![PyPI version](https://badge.fury.io/py/edinet-python.svg)](https://badge.fury.io/py/edinet-python)
[![Build Status](https://travis-ci.org/chakki-works/edinet-python.svg?branch=master)](https://travis-ci.org/chakki-works/edinet-python)
[![codecov](https://codecov.io/gh/chakki-works/edinet-python/branch/master/graph/badge.svg)](https://codecov.io/gh/chakki-works/edinet-python)

* Download the documents from [EDINET](http://disclosure.edinet-fsa.go.jp/).
  * Use official [EDINET API](https://disclosure.edinet-fsa.go.jp/EKW0EZ0015.html).
* Extract contents from XBRL.
  * Main target of parser is annual reports.

## How to use

### Install

```
pip install edinet-python
```

### Download the documents from [EDINET](http://disclosure.edinet-fsa.go.jp/).

#### Get document list of specific day

```py
import edinet


documents = edinet.api.documents.get("2019-01-31")
print(f"Number of documents is {len(documents.list)}")
print(f"Title of first document is {documents.list[0].title}")
```

when only getting the list metadata (number of documents).

```py
import edinet


metadata = edinet.api.metadata.get("2019-01-31")
print(f"Number of documents is {metadata.count}")

```

#### Get document by document id

```py
from pathlib import Path
import edinet


xbrl_path = edinet.api.document.get_xbrl("S100FGR9", save_dir=Path.cwd())
pdf_path = edinet.api.document.get_pdf("S100FGR9", save_dir=Path.cwd())
```

### Extract contents from XBRL

Following aspects are supported. The format is based on `三号様式` that is commonly used for annual report.

0. 文書情報: `Metadata`
    1. 会計年度: `fiscal_year`
    2. 会計期間種別: `fiscal_period_type`
1. 企業の概況: `Company`
    1. 主要な経営指標等の推移
    2. 沿革: `history`
    3. 事業の内容: `business_description`
    4. 関係会社の状況: `affiliated_entities`
    5. 従業員の状況: `employees`
2. 事業の状況: `Business`
    1. 経営方針、経営環境及び対処すべき課題等: `policy_environment_issue_etc`
    2. 事業等のリスク: `risks`
    3. 経営者による財政状態、経営成績及びキャッシュ・フローの状況の分析
    4. 経営上の重要な契約等
    5. 研究開発活動: `research_and_development`
3. 設備の状況
    1. 設備投資等の概要
    2. 主要な設備の状況
    3. 設備の新設、除却等の計画
    4. 賃貸資産
    5. 自社用資産
4. 提出会社の状況: `InformationAboutCompany`
    1. 株式等の状況:
        * 所有者別状況: `shareholders`
    2. 配当政策: `dividend_policy`
    3. 役員の状況: `directors`
    4. コーポレート・ガバナンスの状況等: `corporate_governance`
5. 経理の状況
    1. 連結財務諸表等
    2. 財務諸表等
        * 注記: `notes`
        * 会計方針の変更: `changes_in_accounting_policies`
        * セグメント情報等: `segment_information`
        * 賃貸等不動産関係: `real_estate_for_lease`
    3. 最近の財務諸表
6. 提出会社の株式事務の概要
7. 株式公開情報
    1. 特別利害関係者等の株式等の移動状況
    2. 第三者割当等の概況
    3. 株主の状況
8. 提出会社の参考情報
    1. 提出会社の親会社等の情報
    2. その他の参考情報 

from datetime import datetime


class Document():

    def __init__(self,
                 sequential_no=1,
                 document_id="S1000001",
                 edinet_code="E10001",
                 sec_code="10000",
                 jcn="0000000000001",
                 filer_name="xx株式会社",
                 fund_code="G00001",
                 ordinance_code="000",
                 form_code="000000",
                 doc_type_code="000",
                 period_start="1000-01-01",
                 period_end="1000-01-01",
                 submitted_date="1000-01-01 12:01",
                 title="",
                 issuer_edinet_code="",
                 subject_edinet_code="",
                 subsidiary_edinet_code="",
                 submit_reason="",
                 parent_document_id="",
                 operated_date="1000-01-01 12:01",
                 withdraw_status=0,
                 operation_status=0,
                 disclosure_status=0,
                 has_xbrl=False,
                 has_pdf=False,
                 has_attachment=False,
                 include_english=False
                 ):
        self.sequential_no = sequential_no
        self.document_id = document_id
        self.edinet_code = edinet_code
        self.sec_code = sec_code
        self.jcn = jcn
        self.filer_name = filer_name
        self.fund_code = fund_code
        self.ordinance_code = ordinance_code
        self.form_code = form_code
        self.doc_type_code = doc_type_code
        self.period_start = period_start
        self.period_end = period_end
        self.submitted_date = submitted_date
        self.title = title
        self.issuer_edinet_code = issuer_edinet_code
        self.subject_edinet_code = subject_edinet_code
        self.subsidiary_edinet_code = subsidiary_edinet_code
        self.submit_reason = submit_reason
        self.parent_document_id = parent_document_id
        self.operated_date = operated_date
        self.withdraw_status = withdraw_status
        self.operation_status = operation_status
        self.disclosure_status = disclosure_status
        self.has_xbrl = has_xbrl
        self.has_pdf = has_pdf
        self.has_attachment = has_attachment
        self.include_english = include_english

    @classmethod
    def create(cls, body: dict) -> "Document":
        def to_date(value, format):
            if value:
                f = "%Y-%m-%d" if format == "ymd" else "%Y-%m-%d %H:%M"
                return datetime.strptime(value, f)
            else:
                return None

        def to_bool(value):
            return True if value == "1" else False

        instance = cls(
            sequential_no=body["seqNumber"],
            document_id=body["docID"],
            edinet_code=body["edinetCode"],
            sec_code=body["secCode"],
            jcn=body["JCN"],
            filer_name=body["filerName"],
            fund_code=body["fundCode"],
            ordinance_code=body["ordinanceCode"],
            form_code=body["formCode"],
            doc_type_code=body["docTypeCode"],
            period_start=to_date(body["periodStart"], "ymd"),
            period_end=to_date(body["periodEnd"], "ymd"),
            submitted_date=to_date(body["submitDateTime"], "ymd_hm"),
            title=body["docDescription"],
            issuer_edinet_code=body["issuerEdinetCode"],
            subject_edinet_code=body["subjectEdinetCode"],
            subsidiary_edinet_code=body["subsidiaryEdinetCode"],
            submit_reason=body["currentReportReason"],
            parent_document_id=body["parentDocID"],
            operated_date=to_date(body["opeDateTime"], "ymd_hm"),
            withdraw_status=int(body["withdrawalStatus"]),
            operation_status=int(body["docInfoEditStatus"]),
            disclosure_status=int(body["disclosureStatus"]),
            has_xbrl=to_bool(body["xbrlFlag"]),
            has_pdf=to_bool(body["pdfFlag"]),
            has_attachment=to_bool(body["attachDocFlag"]),
            include_english=to_bool(body["englishDocFlag"])
        )

        return instance

    @property
    def is_outdated(self):
        if not self.edinet_code and self.withdraw_status == 0:
            return True
        else:
            return False

    @property
    def is_withdrew(self):
        if not self.edinet_code and self.withdraw_status == 2:
            return True
        else:
            return False

    def get_pdf(self, save_dir: str = "", file_name: str = ""):
        from edinet.client.document_client import DocumentClient
        client = DocumentClient()
        return client.get_pdf(self.document_id, save_dir, file_name)

    def get_xbrl(self, lang: str = "ja",
                 save_dir: str = "", file_name: str = ""):
        from edinet.client.document_client import DocumentClient
        client = DocumentClient()
        return client.get_xbrl(self.document_id, lang, save_dir, file_name)

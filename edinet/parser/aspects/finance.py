from edinet.parser.xbrl_parser import XBRLParser


class Finance(XBRLParser):
    TAGS = {
        "voluntary_accounting_policy_change": "jpcrp_cor:NotesVoluntaryChangesInAccountingPoliciesConsolidatedFinancialStatementsTextBlock",
        "segment_information": "jpcrp_cor:NotesSegmentInformationEtcConsolidatedFinancialStatementsTextBlock",
        "real_estate_for_lease": "jpcrp_cor:NotesRealEstateForLeaseEtcFinancialStatementsTextBlock"
    }

    def __init__(self, element):
        super().__init__(element)
        self._retrieved = {}

    @property
    def voluntary_accounting_policy_change(self):
        return self.get_document_feature("voluntary_accounting_policy_change")

    @property
    def segment_information(self):
        return self.get_document_feature("segment_information")

    @property
    def real_estate_for_lease(self):
        return self.get_document_feature("real_estate_for_lease")

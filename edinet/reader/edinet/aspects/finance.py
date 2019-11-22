from edinet.reader.base_parser import BaseParser


class Finance(BaseParser):

    def __init__(self, reader):
        tags = {
            "voluntary_accounting_policy_change": "jpcrp_cor:NotesVoluntaryChangesInAccountingPoliciesConsolidatedFinancialStatementsTextBlock",
            "segment_information": "jpcrp_cor:NotesSegmentInformationEtcConsolidatedFinancialStatementsTextBlock",
            "real_estate_for_lease": "jpcrp_cor:NotesRealEstateForLeaseEtcFinancialStatementsTextBlock"
        }

        super().__init__(reader, tags)

    @property
    def voluntary_accounting_policy_change(self):
        return self.get_text_value("voluntary_accounting_policy_change")

    @property
    def segment_information(self):
        return self.get_text_value("segment_information")

    @property
    def real_estate_for_lease(self):
        return self.get_text_value("real_estate_for_lease")

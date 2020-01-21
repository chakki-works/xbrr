import warnings
from xbrr.base.reader.base_parser import BaseParser
from xbrr.edinet.reader.element_value import ElementValue


class Finance(BaseParser):

    def __init__(self, reader):
        tags = {
            "voluntary_accounting_policy_change": "jpcrp_cor:NotesVoluntaryChangesInAccountingPoliciesConsolidatedFinancialStatementsTextBlock",
            "segment_information": "jpcrp_cor:NotesSegmentInformationEtcConsolidatedFinancialStatementsTextBlock",
            "real_estate_for_lease": "jpcrp_cor:NotesRealEstateForLeaseEtcFinancialStatementsTextBlock"
        }

        super().__init__(reader, ElementValue, tags)

    @property
    def use_IFRS(self):
        if "jpigp_cor" in self.reader.namespaces:
            return True
        else:
            return False

    def bs(self, ifrs=False, link_type="calculation"):
        role_uri = "http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_BalanceSheet"
        if ifrs and self.use_IFRS:
            role_uri = "http://disclosure.edinet-fsa.go.jp/role/jpigp/rol_ConsolidatedStatementOfFinancialPositionIFRS"

        bs = self.reader.read_value_by_role(role_uri, link_type)
        return self.__filter_duplicate(bs)

    def pl(self, ifrs=False, link_type="calculation"):
        role_uri = "http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_StatementOfIncome"
        if ifrs and self.use_IFRS:
            role_uri = "http://disclosure.edinet-fsa.go.jp/role/jpigp/rol_ConsolidatedStatementOfComprehensiveIncomeSingleStatementIFRS"
        pl = self.reader.read_value_by_role(role_uri, link_type)
        return self.__filter_duplicate(pl)

    def __filter_duplicate(self, data):
        # Exclude dimension member
        data.drop_duplicates(subset=("name", "period"), keep="first",
                             inplace=True)
        return data

    @property
    def voluntary_accounting_policy_change(self):
        return self.get_text_value("voluntary_accounting_policy_change")

    @property
    def segment_information(self):
        return self.get_text_value("segment_information")

    @property
    def real_estate_for_lease(self):
        return self.get_text_value("real_estate_for_lease")

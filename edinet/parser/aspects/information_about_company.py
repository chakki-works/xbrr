from edinet.parser.xbrl_parser import XBRLParser


class InformationAboutCompany(XBRLParser):
    TAGS = {
        "shareholders": "jpcrp_cor:ShareholdingByShareholderCategoryTextBlock",
        "dividend_policy": "jpcrp_cor:DividendPolicyTextBlock",
        "directors": "jpcrp_cor:InformationAboutOfficersTextBlock",
        "corporate_governance": "jpcrp_cor:ExplanationAboutCorporateGovernanceTextBlock"
    }

    def __init__(self, element):
        super().__init__(element)
        self._retrieved = {}

    @property
    def shareholders(self):
        return self.get_document_feature("shareholders")

    @property
    def dividend_policy(self):
        return self.get_document_feature("dividend_policy")

    @property
    def directors(self):
        return self.get_document_feature("directors")

    @property
    def corporate_governance(self):
        return self.get_document_feature("corporate_governance")

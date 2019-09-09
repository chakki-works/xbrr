from edinet.parser.xbrl_parser import XBRLParser
from edinet.parser.xbrl_feature import XBRLFeature


class Information(XBRLParser):
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

    @property
    def number_of_directors(self):
        numbers, ground = self._extract_number_of_directors()
        return XBRLFeature.integer(numbers["total"], ground=ground)

    @property
    def number_of_female_executives(self):
        numbers, ground = self._extract_number_of_directors()
        return XBRLFeature.integer(numbers["female"], ground=ground)

    def _extract_number_of_directors(self):
        text = self.search_text("^(男性).+(名).+(女性).+(名)")
        numbers = {
            "male": 0,
            "female": 0,
            "total": 0,
        }

        total = 0
        for p, s in [("男性", "名"), ("女性", "名")]:
            value = self.extract_value(p, s)
            if p == "男性":
                numbers["male"] = value
            elif p == "女性":
                numbers["female"] = value
            total += value

        numbers["total"] = total
        return numbers, text

from edinet.parser.base_aspect import BaseAspect
from edinet.document.xbrl_value import XBRLValue


class Information(BaseAspect):
    TAGS = {
        "shareholders": "jpcrp_cor:ShareholdingByShareholderCategoryTextBlock",
        "dividend_policy": "jpcrp_cor:DividendPolicyTextBlock",
        "directors": "jpcrp_cor:InformationAboutOfficersTextBlock",
        "corporate_governance": "jpcrp_cor:ExplanationAboutCorporateGovernanceTextBlock"
    }

    def __init__(self, reader):
        super().__init__(reader)
        self._retrieved = {}

    @property
    def shareholders(self):
        return self.get_text_value("shareholders")

    @property
    def dividend_policy(self):
        return self.get_text_value("dividend_policy")

    @property
    def directors(self):
        return self.get_text_value("directors")

    @property
    def corporate_governance(self):
        return self.get_text_value("corporate_governance")

    @property
    def number_of_directors(self):
        numbers, ground = self._extract_number_of_directors()
        return XBRLValue.integer(numbers["total"], ground=ground)

    @property
    def number_of_female_executives(self):
        numbers, ground = self._extract_number_of_directors()
        return XBRLValue.integer(numbers["female"], ground=ground)

    def _extract_number_of_directors(self):
        parser = self.get_parser("directors")
        text = parser.search("^(男性).+(名).+(女性).+(名)")
        numbers = {
            "male": 0,
            "female": 0,
            "total": 0,
        }

        total = 0
        for p, s in [("男性", "名"), ("女性", "名")]:
            value = parser.extract_value(p, s)
            if p == "男性":
                numbers["male"] = value
            elif p == "女性":
                numbers["female"] = value
            total += value

        numbers["total"] = total
        return numbers, text

from xbrr.base.reader.base_parser import BaseParser
from xbrr.edinet.reader.element_value import ElementValue


class Information(BaseParser):

    def __init__(self, reader):
        tags = {
            "shareholders": "jpcrp_cor:ShareholdingByShareholderCategoryTextBlock",
            "dividend_policy": "jpcrp_cor:DividendPolicyTextBlock",
            "directors": "jpcrp_cor:InformationAboutOfficersTextBlock",
            "corporate_governance": "jpcrp_cor:ExplanationAboutCorporateGovernanceTextBlock"
        }
        super().__init__(reader, ElementValue, tags)

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
        value = self.get_text_value("directors")
        numbers, ground = self._extract_number_of_directors()
        value.value = numbers["total"]
        value.ground = ground
        return value

    @property
    def number_of_female_executives(self):
        value = self.get_text_value("directors")
        numbers, ground = self._extract_number_of_directors()
        value.value = numbers["female"]
        value.ground = ground
        return value

    def _extract_number_of_directors(self):
        text = self.search("directors", "^(男性).+(名).+(女性).+(名)")
        numbers = {
            "male": 0,
            "female": 0,
            "total": 0,
        }

        total = 0
        for p, s in [("男性", "名"), ("女性", "名")]:
            value = self.extract_value("directors", p, s)
            if p == "男性":
                numbers["male"] = value
            elif p == "女性":
                numbers["female"] = value
            total += value

        numbers["total"] = total
        return numbers, text

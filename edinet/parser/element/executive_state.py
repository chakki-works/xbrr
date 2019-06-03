import edinet.parser.item_extractor as ie
from edinet.parser.element.base_feature import BaseFeature


class ExecutiveState(BaseFeature):
    TARGET = "jpcrp_cor:InformationAboutOfficersTextBlock"

    def __init__(self, xbrl_file):
        super().__init__(xbrl_file)
        self._element = self.xbrl_file.get_document(self.TARGET).html

    @property
    def number_of_executives(self):
        numbers, ground = self._extract_number_of_executives()
        return numbers["total"], ground

    @property
    def percentage_of_female_executives(self):
        numbers, ground = self._extract_number_of_executives()
        value = 0.0
        if numbers["female"] > 0:
            value = numbers["female"] / numbers["total"]

        return value, ground

    def _extract_number_of_executives(self):
        matcher = ie.TextContextMatcher("^(男性).+(名).+(女性).+(名)")
        text = matcher.search(self._element)

        numbers = {
            "male": 0,
            "female": 0,
            "total": 0,
        }

        total = 0
        for p, s in [("男性", "名"), ("女性", "名")]:
            extractor = ie.TextValueExtractor(p, s)
            value = extractor.extract(text)
            if p == "男性":
                numbers["male"] = value
            elif p == "女性":
                numbers["female"] = value
            total += value

        numbers["total"] = total

        return numbers, text

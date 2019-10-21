from datetime import datetime
from edinet.parser.xbrl_parser import XBRLParser
from edinet.xbrl_feature import XBRLFeature


class Metadata(XBRLParser):
    TAGS = {
        "fiscal_date": "jpdei_cor:CurrentFiscalYearStartDateDEI",
        "fiscal_period_kind": "jpdei_cor:TypeOfCurrentPeriodDEI",
        "name": "jpcrp_cor:CompanyNameCoverPage",
        "name_en": "jpcrp_cor:CompanyNameInEnglishCoverPage",
        "address": "jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage",
        "phone_number": "jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage"
    }

    def __init__(self, element):
        super().__init__(element)
        self._retrieved = {}

        for k in self.TAGS:
            self._retrieved[k] = self._element.find(self.TAGS[k])
            if self._retrieved[k]:
                ground = self._retrieved[k].text
                value = self.normalize(ground)
                self._retrieved[k] = (value, ground)

    @property
    def fiscal_year(self):
        value, ground = self._retrieved["fiscal_date"]
        if value:
            date = datetime.strptime(value, "%Y-%m-%d")
            value = date.year
        feature = XBRLFeature.integer(value=value, ground=ground)
        return feature

    @property
    def fiscal_month(self):
        value, ground = self._retrieved["fiscal_date"]
        if value:
            date = datetime.strptime(value, "%Y-%m-%d")
            value = date.month
        feature = XBRLFeature.integer(value=value, ground=ground)
        return feature

    @property
    def fiscal_period_kind(self):
        value, ground = self._retrieved["fiscal_period_kind"]
        feature = XBRLFeature.category(value=value, ground=ground)
        return feature

    @property
    def company_name(self):
        value, ground = self._retrieved["name"]
        feature = XBRLFeature.text(value=value, ground=ground)
        return feature

    @property
    def company_name_en(self):
        value, ground = self._retrieved["name_en"]
        feature = XBRLFeature.text(value=value, ground=ground)
        return feature

    @property
    def address(self):
        value, ground = self._retrieved["address"]
        feature = XBRLFeature.text(value=value, ground=ground)
        return feature

    @property
    def phone_number(self):
        value, ground = self._retrieved["phone_number"]
        feature = XBRLFeature.text(value=value, ground=ground)
        return feature

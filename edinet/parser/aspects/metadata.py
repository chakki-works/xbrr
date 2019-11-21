from datetime import datetime
from edinet.parser.base_aspect import BaseAspect
from edinet.document.xbrl_value import XBRLValue


class Metadata(BaseAspect):
    TAGS = {
        "fiscal_date": "jpdei_cor:CurrentFiscalYearStartDateDEI",
        "fiscal_period_kind": "jpdei_cor:TypeOfCurrentPeriodDEI",
        "name": "jpcrp_cor:CompanyNameCoverPage",
        "name_en": "jpcrp_cor:CompanyNameInEnglishCoverPage",
        "address": "jpcrp_cor:AddressOfRegisteredHeadquarterCoverPage",
        "phone_number": "jpcrp_cor:TelephoneNumberAddressOfRegisteredHeadquarterCoverPage"
    }

    def __init__(self, reader):
        super().__init__(reader)
        self._retrieved = {}

        for k in self.TAGS:
            parser = self.get_parser(k)
            element = parser.element.element
            if element:
                ground = element.text
                value = parser.normalize(ground)
                self._retrieved[k] = (value, ground)

    @property
    def fiscal_year(self):
        value, ground = self._retrieved["fiscal_date"]
        if value:
            date = datetime.strptime(value, "%Y-%m-%d")
            value = date.year
        feature = XBRLValue.integer(value=value, ground=ground)
        return feature

    @property
    def fiscal_month(self):
        value, ground = self._retrieved["fiscal_date"]
        if value:
            date = datetime.strptime(value, "%Y-%m-%d")
            value = date.month
        feature = XBRLValue.integer(value=value, ground=ground)
        return feature

    @property
    def fiscal_period_kind(self):
        value, ground = self._retrieved["fiscal_period_kind"]
        feature = XBRLValue.category(value=value, ground=ground)
        return feature

    @property
    def company_name(self):
        value, ground = self._retrieved["name"]
        feature = XBRLValue.text(value=value, ground=ground)
        return feature

    @property
    def company_name_en(self):
        value, ground = self._retrieved["name_en"]
        feature = XBRLValue.text(value=value, ground=ground)
        return feature

    @property
    def address(self):
        value, ground = self._retrieved["address"]
        feature = XBRLValue.text(value=value, ground=ground)
        return feature

    @property
    def phone_number(self):
        value, ground = self._retrieved["phone_number"]
        feature = XBRLValue.text(value=value, ground=ground)
        return feature

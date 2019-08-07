from datetime import datetime
from edinet.parser.aspects.base_feature import BaseFeature, Value


class CurrentPeriod(BaseFeature):
    YEAR = "jpdei_cor:CurrentFiscalYearStartDateDEI"
    KIND = "jpdei_cor:TypeOfCurrentPeriodDEI"

    def __init__(self, xbrl_file):
        super().__init__(xbrl_file)
        self._year = self.xbrl_file.get_document(self.YEAR).html
        self._kind = self.xbrl_file.get_document(self.KIND).html

    @property
    def fiscal_year(self):
        text = self._year.text.strip()
        date = datetime.strptime(text, "%Y-%m-%d")
        value = Value(value=date.year, unit="NUM", ground=text)
        return value

    @property
    def fiscal_period_type(self):
        text = self._kind.text.strip()
        value = Value(value=text, unit="CAT", ground=text)
        return value

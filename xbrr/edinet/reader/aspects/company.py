from xbrr.base.reader.base_parser import BaseParser
from xbrr.edinet.reader.element_value import ElementValue


class Company(BaseParser):

    def __init__(self, reader):
        tags = {
            "history": "jpcrp_cor:CompanyHistoryTextBlock",
            "business_description": "jpcrp_cor:DescriptionOfBusinessTextBlock",
            "affiliated_entities": "jpcrp_cor:OverviewOfAffiliatedEntitiesTextBlock",
            "employees": "jpcrp_cor:InformationAboutEmployeesTextBlock"
        }
        super().__init__(reader, ElementValue, tags)

    @property
    def history(self):
        return self.get_text_value("history")

    @property
    def business_description(self):
        return self.get_text_value("business_description")

    @property
    def affiliated_entities(self):
        return self.get_text_value("affiliated_entities")

    @property
    def employees(self):
        return self.get_text_value("employees")

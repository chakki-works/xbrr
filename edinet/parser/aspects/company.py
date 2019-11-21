from edinet.parser.base_aspect import BaseAspect


class Company(BaseAspect):
    TAGS = {
        "history": "jpcrp_cor:CompanyHistoryTextBlock",
        "business_description": "jpcrp_cor:DescriptionOfBusinessTextBlock",
        "affiliated_entities": "jpcrp_cor:OverviewOfAffiliatedEntitiesTextBlock",
        "employees": "jpcrp_cor:InformationAboutEmployeesTextBlock"
    }

    def __init__(self, reader):
        super().__init__(reader)
        self._retrieved = {}

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

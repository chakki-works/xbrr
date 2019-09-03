from edinet.parser.xbrl_parser import XBRLParser


class Company(XBRLParser):
    TAGS = {
        "history": "jpcrp_cor:CompanyHistoryTextBlock",
        "business_description": "jpcrp_cor:DescriptionOfBusinessTextBlock",
        "affiliated_entities": "jpcrp_cor:OverviewOfAffiliatedEntitiesTextBlock",
        "employees": "jpcrp_cor:InformationAboutEmployeesTextBlock"
    }

    def __init__(self, element):
        super().__init__(element)
        self._retrieved = {}

    @property
    def history(self):
        return self.get_document_feature("history")

    @property
    def business_description(self):
        return self.get_document_feature("business_description")

    @property
    def affiliated_entities(self):
        return self.get_document_feature("affiliated_entities")

    @property
    def employees(self):
        return self.get_document_feature("employees")

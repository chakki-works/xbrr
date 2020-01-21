from xbrr.base.reader.base_parser import BaseParser
from xbrr.edinet.reader.element_value import ElementValue


class Business(BaseParser):

    def __init__(self, reader):
        tags = {
            "policy_environment_issue_etc": "jpcrp_cor:BusinessPolicyBusinessEnvironmentIssuesToAddressEtcTextBlock",
            "risks": "jpcrp_cor:BusinessRisksTextBlock",
            "research_and_development": "jpcrp_cor:ResearchAndDevelopmentActivitiesTextBlock",
            "management_analysis": "jpcrp_cor:ManagementAnalysisOfFinancialPositionOperatingResultsAndCashFlowsTextBlock",
            "overview_of_result": "jpcrp_cor:OverviewOfBusinessResultsTextBlock",
            "overview_of_value_chain": "jpcrp_cor:OverviewOfProductionOrdersReceivedAndSalesTextBlock",
            "analysis_of_finance": "jpcrp_cor:AnalysisOfFinancialPositionOperatingResultsAndCashFlowsTextBlock"
        }
        super().__init__(reader, ElementValue, tags)

    @property
    def policy_environment_issue_etc(self):
        return self.get_text_value("policy_environment_issue_etc")

    @property
    def risks(self):
        return self.get_text_value("risks")

    @property
    def management_analysis(self):
        return self.get_text_value("management_analysis")

    @property
    def research_and_development(self):
        return self.get_text_value("research_and_development")

    @property
    def overview_of_result(self):
        return self.get_text_value("overview_of_result")

    @property
    def overview_of_value_chain(self):
        return self.get_text_value("overview_of_value_chain")

    @property
    def analysis_of_finance(self):
        return self.get_text_value("analysis_of_finance")

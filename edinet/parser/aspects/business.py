from edinet.parser.xbrl_parser import XBRLParser


class Business(XBRLParser):
    TAGS = {
        "policy_environment_issue_etc": "jpcrp_cor:BusinessPolicyBusinessEnvironmentIssuesToAddressEtcTextBlock",
        "risks": "jpcrp_cor:BusinessRisksTextBlock",
        "research_and_development": "jpcrp_cor:ResearchAndDevelopmentActivitiesTextBlock",
        "management_analysis": "jpcrp_cor:ManagementAnalysisOfFinancialPositionOperatingResultsAndCashFlowsTextBlock",
        "overview_of_result": "jpcrp_cor:OverviewOfBusinessResultsTextBlock",
        "overview_of_value_chain": "jpcrp_cor:OverviewOfProductionOrdersReceivedAndSalesTextBlock",
        "analysis_of_finance": "jpcrp_cor:AnalysisOfFinancialPositionOperatingResultsAndCashFlowsTextBlock"
    }

    def __init__(self, element):
        super().__init__(element)
        self._retrieved = {}

    @property
    def policy_environment_issue_etc(self):
        return self.get_document_feature("policy_environment_issue_etc")

    @property
    def risks(self):
        return self.get_document_feature("risks")

    @property
    def management_analysis(self):
        return self.get_document_feature("management_analysis")

    @property
    def research_and_development(self):
        return self.get_document_feature("research_and_development")

    @property
    def overview_of_result(self):
        return self.get_document_feature("overview_of_result")

    @property
    def overview_of_value_chain(self):
        return self.get_document_feature("overview_of_value_chain")

    @property
    def analysis_of_finance(self):
        return self.get_document_feature("analysis_of_finance")

from edinet.parser.xbrl_parser import XBRLParser


class Business(XBRLParser):
    TAGS = {
        "policy_environment_issue_etc": "jpcrp_cor:BusinessPolicyBusinessEnvironmentIssuesToAddressEtcTextBlock",
        "risks": "jpcrp_cor:BusinessRisksTextBlock",
        "research_and_development": "jpcrp_cor:ResearchAndDevelopmentActivitiesTextBlock"
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
    def research_and_development(self):
        return self.get_document_feature("research_and_development")

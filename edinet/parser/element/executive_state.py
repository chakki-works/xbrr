class ExecutiveStateParser():
    TARGET = "jpcrp_cor:InformationAboutOfficersTextBlock"

    def __init__(self, xbrl_file):
        self.xbrl_file = xbrl_file

    def parse(self):
        html = self.xbrl_file.get_document(self.TARGET).html
        return html

import os
import unittest
from xbrr.edinet.client.document_client import DocumentClient
from xbrr.edinet.reader.directory import Directory


class TestDirectory(unittest.TestCase):

    def test_xbrl_dir(self):
        _dir = os.path.join(os.path.dirname(__file__), "../data")
        client = DocumentClient()
        file_path = client.get_xbrl("S100FGR9", save_dir=_dir,
                                    expand_level="dir")
        xbrl_dir = Directory(file_path)

        self.assertGreater(len(xbrl_dir.xsd.find_all("element")), 0)
        self.assertGreater(len(xbrl_dir.cal.find_all("calculationLink")), 0)
        self.assertGreater(len(xbrl_dir.def_.find_all("definitionArc")), 0)
        self.assertGreater(len(xbrl_dir.lab.find_all("labelLink")), 0)
        self.assertGreater(len(xbrl_dir.lab_en.find_all("labelLink")), 0)
        self.assertGreater(len(xbrl_dir.pre.find_all("presentationLink")), 0)
        self.assertTrue(xbrl_dir.man.find("manifest"))

        xbrl_dir.delete()
        self.assertFalse(os.path.exists(file_path))

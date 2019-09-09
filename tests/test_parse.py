import os
import unittest
import edinet


class TestParse(unittest.TestCase):

    def test_parse_element(self):
        path = os.path.join(os.path.dirname(__file__),
                            "./data/xbrl2019.xbrl")

        result = edinet.parse(path, "information", "number_of_directors")
        self.assertEqual(result.value, 14)

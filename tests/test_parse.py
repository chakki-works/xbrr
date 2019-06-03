import os
import unittest
import edinet


class TestParse(unittest.TestCase):

    def test_parse_element(self):
        path = os.path.join(os.path.dirname(__file__),
                            "./data/test_example_1.xbrl")

        data = {
            "company": "xxxx",
            "from_ym": "2018/4",
            "to_ym": "2019/3",
        }

        result = edinet.parse(path, "executive_state", "number_of_executives", data)
        self.assertEqual(result["company"], "xxxx")
        self.assertEqual(result["number_of_executives"]["value"], 14)

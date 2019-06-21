import os
import unittest
import edinet


class TestParse(unittest.TestCase):

    def test_parse_element(self):
        path = os.path.join(os.path.dirname(__file__),
                            "./data/test_example_1.xbrl")

        result = edinet.parse(path, "executive_state", "number_of_executives")
        self.assertEqual(result.value, 14)

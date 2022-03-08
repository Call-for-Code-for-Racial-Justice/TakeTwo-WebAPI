from json import load
import sys
sys.path.append('../../taketwo-webapi')
sys.path.append('../util')
import unittest
from unittest.mock import patch

from main import analyse_text
from main import Text

from util.mock_db_util import getRow
from util.mock_db_util import setupMocks

class TestAnalyseText(unittest.TestCase):

    @patch('main.getDb')
    def test_multiple_items_with_flagged_string(self, getDbMock):
        firstRow = getRow("bad_string", "the_category", "the_info")
        secondRow = getRow("bad_string_2", "the_category", "the_info")
        
        setupMocks(getDbMock, [firstRow, secondRow])

        data = {'content': 'bad_string, bad_string_2'}
        text = Text(**data)
        output = analyse_text(text)

        expected = {"biased": 
                        [{"flag": "bad_string", "category": "the_category", "info": "the_info"},
                         {"flag": "bad_string_2", "category": "the_category", "info": "the_info"}]}
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    @patch('main.getDb')
    def test_single_item_with_flagged_string(self, getDbMock):
        firstRow = getRow("bad_string", "the_category", "the_info")
        
        setupMocks(getDbMock, [firstRow])

        data = {'content': 'bad_string'}
        text = Text(**data)
        output = analyse_text(text)

        expected = {"biased": 
                        [{"flag": "bad_string", "category": "the_category", "info": "the_info"}]}
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    @patch('main.getDb')
    def test_no_text_provided(self, getDbMock):
        firstRow = getRow("bad_string", "the_category", "the_info")
        
        setupMocks(getDbMock, [firstRow])

        data = {'content': ''}
        text = Text(**data)
        output = analyse_text(text)

        expected = {"biased": []}
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

if __name__ == '__main__':
    unittest.main()
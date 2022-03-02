from json import load
import sys
sys.path.append('../../taketwo-webapi')
sys.path.append('../util')
import unittest
from unittest.mock import patch

from main import check_words
from main import Text

from util.mock_db_util import getRow
from util.mock_db_util import setupMocks

class TestCheckWords(unittest.TestCase):

    @patch('main.getDb')
    def test_no_text_provided(self, getDbMock):
        firstRow = getRow("bad_string", "racial slur", "the_info")

        setupMocks(getDbMock, [firstRow])

        data = {'content': ''}
        text = Text(**data)
        output = check_words(text)

        expected = []
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    @patch('main.getDb')
    def test_single_flagged_string_in_content(self,getDbMock):
        firstRow = getRow("bad_string", "racial slur", "the_info")

        setupMocks(getDbMock, [firstRow])

        data = {'content': 'bad_string'}
        text = Text(**data)
        output = check_words(text)

        expected = [{"line":1, "word":"bad_string", "additional_info":"the_info"}]
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    @patch('main.getDb')
    def test_single_flagged_string_and_valid_string_in_content(self,getDbMock):
        firstRow = getRow("bad_string", "racial slur", "the_info")

        setupMocks(getDbMock, [firstRow])

        data = {'content': 'bad_string\nokay_string'}
        text = Text(**data)
        output = check_words(text)

        expected = [{"line":1, "word":"bad_string", "additional_info":"the_info"}]
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    @patch('main.getDb')
    def test_multiple_flagged_strings_existing_records(self,getDbMock):

        firstRow = getRow("bad_string", "racial slur", "the_info")
        secondRow = getRow("bad_string_2", "racial slur", "the_info_2")
        thirdRow = getRow("biased_thing", "other", "the_info_3")

        setupMocks(getDbMock, [firstRow, secondRow, thirdRow])

        data = {'content': 'bad_string\nbad_string_2'}
        text = Text(**data)
        output = check_words(text)

        expected = [{"line":1, "word":"bad_string", "additional_info":"the_info"},
                    {"line":2, "word":"bad_string", "additional_info":"the_info"},
                    {"line":2, "word":"bad_string_2", "additional_info":"the_info_2"}]
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

if __name__ == '__main__':
    unittest.main()

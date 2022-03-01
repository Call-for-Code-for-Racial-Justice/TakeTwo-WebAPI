from json import load
import sys
sys.path.append('../../taketwo-webapi')
sys.path.append('../util')
import unittest
from unittest.mock import MagicMock

from main import check_words
from main import db
from main import Text
from couchdb.client import Document
from couchdb.client import Row

class TestCheckWords(unittest.TestCase):

    def test_no_text_provided(self):
        firstDoc = Document()
        firstDoc["flagged_string"] = "bad_string"
        firstDoc["category"] = "racial slur"
        firstDoc["info"] = "the_info"
        firstRow = Row()
        firstRow['doc'] = firstDoc

        mockDbViewResults = MagicMock()
        mockDbViewResults.__iter__ = MagicMock(return_value=iter([firstRow]))
        db.view = MagicMock(return_value=mockDbViewResults)

        data = {'content': ''}
        text = Text(**data)
        output = check_words(text)

        expected = []
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    def test_single_flagged_string_in_content(self):
        firstDoc = Document()
        firstDoc["flagged_string"] = "bad_string"
        firstDoc["category"] = "racial slur"
        firstDoc["info"] = "the_info"
        firstRow = Row()
        firstRow['doc'] = firstDoc

        mockDbViewResults = MagicMock()
        mockDbViewResults.__iter__ = MagicMock(return_value=iter([firstRow]))
        db.view = MagicMock(return_value=mockDbViewResults)

        data = {'content': 'bad_string'}
        text = Text(**data)
        output = check_words(text)

        expected = [{"line":1, "word":"bad_string", "additional_info":"the_info"}]
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    def test_single_flagged_string_and_valid_string_in_content(self):
        firstDoc = Document()
        firstDoc["flagged_string"] = "bad_string"
        firstDoc["category"] = "racial slur"
        firstDoc["info"] = "the_info"
        firstRow = Row()
        firstRow['doc'] = firstDoc

        mockDbViewResults = MagicMock()
        mockDbViewResults.__iter__ = MagicMock(return_value=iter([firstRow]))
        db.view = MagicMock(return_value=mockDbViewResults)

        data = {'content': 'bad_string\nokay_string'}
        text = Text(**data)
        output = check_words(text)

        expected = [{"line":1, "word":"bad_string", "additional_info":"the_info"}]
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    def test_multiple_flagged_strings_existing_records(self):
        firstDoc = Document()
        firstDoc["flagged_string"] = "bad_string"
        firstDoc["category"] = "racial slur"
        firstDoc["info"] = "the_info"
        firstRow = Row()
        firstRow['doc'] = firstDoc

        secondDoc = Document()
        secondDoc["flagged_string"] = "bad_string_2"
        secondDoc["category"] = "racial slur"
        secondDoc["info"] = "the_info_2"
        secondRow = Row()
        secondRow['doc'] = secondDoc

        thirdDoc = Document()
        thirdDoc["flagged_string"] = "biased_thing"
        thirdDoc["category"] = "other"
        thirdDoc["info"] = "the_info_3"
        thirdRow = Row()
        thirdRow['doc'] = thirdDoc
        mockDbViewResults = MagicMock()
        mockDbViewResults.__iter__ = MagicMock(return_value=iter([firstRow, secondRow, thirdRow]))
        db.view = MagicMock(return_value=mockDbViewResults)

        data = {'content': 'bad_string\nbad_string_2'}
        text = Text(**data)
        output = check_words(text)

        expected = [{"line":1, "word":"bad_string", "additional_info":"the_info"},
                    {"line":2, "word":"bad_string", "additional_info":"the_info"},
                    {"line":2, "word":"bad_string_2", "additional_info":"the_info_2"}]
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

if __name__ == '__main__':
    unittest.main()

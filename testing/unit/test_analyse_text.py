from json import load
import sys
sys.path.append('../../taketwo-webapi')
sys.path.append('../util')
import unittest
from unittest.mock import MagicMock

from main import analyse_text
from main import db
from main import Text
from couchdb.client import Document
from couchdb.client import Row

class TestTakeTwoWebApi(unittest.TestCase):

    def test_multiple_items_with_flagged_string(self):
        firstDoc = Document()
        firstDoc["flagged_string"] = "bad_string"
        firstDoc["category"] = "the_category"
        firstDoc["info"] = "the_info"
        firstRow = Row()
        firstRow['doc'] = firstDoc

        secondDoc = Document()
        secondDoc["flagged_string"] = "bad_string_2"
        secondDoc["category"] = "the_category"
        secondDoc["info"] = "the_info"
        secondRow = Row()
        secondRow['doc'] = secondDoc
        mockDbViewResults = MagicMock()
        mockDbViewResults.__iter__ = MagicMock(return_value=iter([firstRow, secondRow]))
        db.view = MagicMock(return_value=mockDbViewResults)

        data = {'content': 'bad_string, bad_string_2'}
        text = Text(**data)
        output = analyse_text(text)

        expected = {"biased": 
                        [{"flag": "bad_string", "category": "the_category", "info": "the_info"},
                         {"flag": "bad_string_2", "category": "the_category", "info": "the_info"}]}
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    def test_single_item_with_flagged_string(self):
        firstDoc = Document()
        firstDoc["flagged_string"] = "bad_string"
        firstDoc["category"] = "the_category"
        firstDoc["info"] = "the_info"
        firstRow = Row()
        firstRow['doc'] = firstDoc
        mockDbViewResults = MagicMock()
        mockDbViewResults.__iter__ = MagicMock(return_value=iter([firstRow]))
        db.view = MagicMock(return_value=mockDbViewResults)

        data = {'content': 'bad_string'}
        text = Text(**data)
        output = analyse_text(text)

        expected = {"biased": 
                        [{"flag": "bad_string", "category": "the_category", "info": "the_info"}]}
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

    def test_no_items_in_db(self):
        mockDbViewResults = MagicMock()
        mockDbViewResults.__iter__ = MagicMock(return_value=iter([]))
        db.view = MagicMock(return_value=mockDbViewResults)

        data = {'content': 'bad_string'}
        text = Text(**data)
        output = analyse_text(text)

        expected = {"biased": 
                        []}
        assert output == expected, "Actual: " + str(output) + " Expected: " + str(expected)

if __name__ == '__main__':
    unittest.main()
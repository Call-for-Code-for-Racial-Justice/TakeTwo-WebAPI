from couchdb.client import Document
from couchdb.client import Row
from unittest.mock import MagicMock
    
def getRow(flaggedString, category, info):
    firstDoc = Document()
    firstDoc["flagged_string"] = flaggedString
    firstDoc["category"] = category
    firstDoc["info"] = info
    firstRow = Row()
    firstRow['doc'] = firstDoc
    return firstRow

def setupMocks(getDbMock, rows):
    mockDbViewResults = MagicMock()
    mockDbViewResults.return_value = iter(rows)
    dbMock = MagicMock()
    dbMock.view = mockDbViewResults
    getDbMock.return_value=dbMock
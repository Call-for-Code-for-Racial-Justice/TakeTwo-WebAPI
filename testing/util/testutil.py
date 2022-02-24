    
def comparePayloads(expected: dict, actual: dict):
    assert expected["user_id"] == actual["user_id"], showDiff(str(expected["user_id"]), str(actual["user_id"]))
    assert expected["flagged_string"] == actual["flagged_string"], showDiff(str(expected["flagged_string"]), str(actual["flagged_string"]))
    assert expected["category"] == actual["category"], showDiff(str(expected["category"]), str(actual["category"]))
    assert expected["info"] == actual["info"], showDiff(str(expected["info"]), str(actual["info"]))
    assert expected["url"] == actual["url"], showDiff(str(expected["url"]), str(actual["url"]))

def showDiff(expected: str, actual: str):
    return "Expected: " + expected + ", Actual: " + actual
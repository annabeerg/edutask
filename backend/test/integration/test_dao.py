import pytest
import unittest.mock as mock
from unittest.mock import patch

from src.util.dao import DAO

testValidator =     {
"$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "description", "bool_value"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "the title of a task must be determined",
                "uniqueItems": True
            }, 
            "description": {
                "bsonType": "string",
                "description": "the description of a task must be determined"
            },
                "bool_value": {
                "bsonType": "bool",
                "description": "the description of a task must true or false"
            }, 
        }
    }
}
@pytest.fixture
def sut():
    with patch("src.util.dao.getValidator", autospec=True) as mockedGetValidators:
        mockedGetValidators.return_value = testValidator 
        task = DAO(collection_name="testTask")

        yield task
        task.collection.drop()

'''Test if all required properties is present, valid bson data, unique items (only 1 item with same name in document)'''
@pytest.mark.integration
@pytest.mark.parametrize('inputData, expected',
    [
        ({"title": "test if title is string", "description": "test if description is string not need to be unique", "bool_value": True}, dict),
    ]
)
def test_create(sut, inputData,  expected):
    valid_res = sut.create(inputData)
    assert type(valid_res) == expected

"""
Test to see if exception is raised when the validator dont fulfill required properties: 

Test if all required properties is present, invalid bson data, unique items
Test if all required properties is not present, valid bson data, unique items
Test if all required properties is not present, invalid bson data, unique items
Test if all required properties is present, invalid bson data, not unique items
Test if all required properties is present, valid bson data, not unique items
Test if all required properties is not present, valid bson data, not unique items
Test if all required properties is not present, invalid bson data, not unique items
"""
@pytest.mark.integration
@pytest.mark.parametrize('inputData, expected',
    [
        ({"tile": "title", "description": 1, "bool_value": True}, "WriteError"),
        ({"tile": "title", "bool_value": True}, "WriteError"),
        ({"tile": "title", "bool_value": 1}, "WriteError"),
        ({"tile": "", "description": "descrition", "bool_value": True}, "WriteError"),
        ({"tile": "", "description": "descrition", "bool_value": True}, "WriteError"),
        ({"tile": "", "bool_value": True}, "WriteError"),
        ({"tile": "", "bool_value": 1}, "WriteError"),
    ]
)
@pytest.mark.integration
def test_invalid_writeerror(sut, inputData, expected):
    with pytest.raises(Exception) as WriteError:
        sut.create(inputData)
    assert expected in str(WriteError)

import pytest
import unittest.mock as mock

from bson.objectid import ObjectId
from src.util.dao import DAO

@pytest.fixture
def sut():
    saved_task = []
    def task(info):
        created_task = DAO("task").create(info)
        saved_task.append(created_task)
        return created_task
        
    yield task
    for value in saved_task:
        DAO("task").delete(value["_id"]["$oid"])

'''Test if all required properties is present, valid bson data, unique items'''
@pytest.mark.integration
def test_create(sut):
    created = sut({"title": "title", "description": "description", "todo": "add", "requires": [ObjectId("5d6ede6a0ba62570afcedd3b")]})
    assert created["title"] == "title"
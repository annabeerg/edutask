import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

def sut(email: str, alt_email=None):
    if alt_email == None:
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = [{'email': email}]
        return mockedDAO
    elif alt_email == "error":
        mockedDAO = mock.MagicMock()
        mockedDAO.find.side_effect = Exception(None)
        return mockedDAO
    elif alt_email == "empty":
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = []
        return mockedDAO
    else: 
        mockedDAO = mock.MagicMock()
        mockedDAO.find.return_value = [{'email': email}, {'email': alt_email}]
        return mockedDAO

def errorhandler(expected_output: str):
    if expected_output == 'ValueError':
        return 'Error: invalid email address'
    elif expected_output == "None":
        return ''

"""if email is valid"""
@pytest.mark.controller
def test_UserController_validformat():
    daoUsr=sut('jane.doe@gmail.com')
    mockedUser = UserController(dao=daoUsr)
    expected = daoUsr.find()[0]
    assert mockedUser.get_user_by_email(email='jane.doe@gmail.com') == expected

"""if email is valid and its more then 1 user (checking print)"""
@pytest.mark.controller
def test_UserController_multipleUsers(capsys):
    daoUsr=sut('jane.doe@gmail.com', 'jane.doe@gmail.com')
    mockedUser = UserController(dao=daoUsr)
    mockedUser.get_user_by_email(email='jane.doe@gmail.com')
    captured_print = capsys.readouterr()
    assert captured_print.out == 'Error: more than one user found with mail jane.doe@gmail.com\n'

"""if email is valid and its more then 1 user"""
@pytest.mark.controller
def test_UserController_miltiple():
    daoUsr=sut('jane.doe@gmail.com')
    mockedUser = UserController(dao=daoUsr)
    expected = daoUsr.find()[0]
    assert mockedUser.get_user_by_email(email='jane.doe@gmail.com') == expected

"""if database is empty and email is valid"""
@pytest.mark.controller
def test_UserController_emptyvalid():
    daoUsr=sut('', "empty")
    mockedUser = UserController(dao=daoUsr)
    expected = None
    assert mockedUser.get_user_by_email(email='jane.doe@gmail.com') == expected

"""if email is not valid"""
@pytest.mark.controller
def test_UserController_invalidformat():
    daoUsr = None
    mockedUser = UserController(dao=daoUsr)
    with pytest.raises(ValueError) as expected_ValueError:
        mockedUser.get_user_by_email(email='jane.doe')
    assert str(expected_ValueError.value) == errorhandler("ValueError")

"""if the email is not valid"""
@pytest.mark.controller
def test_UserController_notexisting():
    daoUsr = sut('jane.doe@gmail.com', 'error')
    mockedUser = UserController(dao=daoUsr)
    with pytest.raises(Exception) as expected_Exception:
        mockedUser.get_user_by_email(email='jane@gmail.com')
    assert str(expected_Exception.value) == "None"


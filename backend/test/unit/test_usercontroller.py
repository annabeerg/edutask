import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.fixture
def sut(daoList):

        mockedDAO = mock.MagicMock()

        mockedDAO.find.return_value = daoList
  
        mockedReturnValue = UserController(dao=mockedDAO)
        return mockedReturnValue

"""test if first object is returned if email is valid and that None is return if email is valid but not in Database"""
@pytest.mark.unit
@pytest.mark.parametrize('daoList, expected',
    [  
        ([{"email": 'maria@maria.se'}], {"email": 'maria@maria.se'}),
        ([{"email": 'maria@maria.se'}, {"email": 'maria@maria.se'}, {"email": 'maria@maria.se'}], {"email": 'maria@maria.se'}),
        ([], None)
    ]
)
def test_valid_email(sut, expected):
    ValidEmailResult = sut.get_user_by_email(email="maria@maria.se")
   
    assert ValidEmailResult == expected

"""test if Value Error is throen if email is not valid"""
@pytest.mark.unit
@pytest.mark.parametrize('daoList, expected',
    [ 
        ([{"email": 'maria@maria.se'}], {"email": 'maria@maria.se'}),
    ]
)
def test_invalid_email(sut, expected):
    with pytest.raises(ValueError):
        inValidEmailResult = sut.get_user_by_email(email="ihiuhuihx")

        assert inValidEmailResult == expected

"""test if Exception is thrown if database error"""
@pytest.mark.unit
def test_database_error():
    mockedDAO = mock.MagicMock()

    mockedDAO.find.return_value = Exception
  
    mockedReturnValue = UserController(dao=mockedDAO)
     
    with pytest.raises(Exception):
          expected = {"email": 'maria@maria.se'}
          databaseErrorResult = mockedReturnValue.get_user_by_email(email="maria@maria.se")
    
          assert databaseErrorResult == expected


"""Extra test for checking the print statement when """
@pytest.mark.unit
def test_UserController_multipleUsers(capsys):
    mockedDAO = mock.MagicMock()

    mockedDAO.find.return_value = [{"email": 'maria@maria.se'}, {"email": 'maria@maria.se'}, {"email": 'maria@maria.se'}]
  
    mockedUser = UserController(dao=mockedDAO)
     
    mockedUser.get_user_by_email(email='maria@maria.se')
    captured_print = capsys.readouterr()
    assert captured_print.out == 'Error: more than one user found with mail maria@maria.se\n'
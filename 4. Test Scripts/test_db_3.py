import sys
sys.path.append('../')

import DatabaseConnection
import User

def test_add_user_3():

    test_user = User.User.get_user( 'jfj','top',None)
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db_3')
    assert db.add_user(test_user) == False

def test_add_user_4():
    test_user = User.User.get_user( 'jfj',None,'top')
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db')
    assert db.add_user(test_user) == False

def test_add_user_5():
    test_user = User.User.get_user( None, 'jfj','top')
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db')
    db.remove_user()
    assert db.add_user(test_user) == False
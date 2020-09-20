import sys
sys.path.append('../')

import DatabaseConnection
import User

def test_add_user_1():
    test_user = User.User.get_user('awdad','dsdfkjfka', 'jdkfak')
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db_2')
    db.add_user(test_user)
    test_user2 = User.User.get_user('awfsdfdad', 'dsdfsdfskjfka', 'jdksdffak')
    assert db.add_user(test_user2) == False
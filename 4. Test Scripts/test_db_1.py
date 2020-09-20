import sys
sys.path.append('../')

import DatabaseConnection

def test_cons():
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db_1')
    db1 = DatabaseConnection.DatabaseConnection.get_connection('test_db')
    # assuring only one databae connection is created.
    assert db == db1
    assert db.connection != None
    assert db.cursor != None


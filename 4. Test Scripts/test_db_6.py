import sys
sys.path.append('../')

import DatabaseConnection

def test_get_a_recipint():
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db_6')
    assert db.get_contact('ksajh') == []
    assert db.get_contact(None) == []

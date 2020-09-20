import sys
sys.path.append('../')

import DatabaseConnection
import Contact

def test_contact_3():

    test_contact = Contact.Contact( 'jfj','top',None)
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db_4')
    assert db.add_contact(test_contact) == False

def test_contact_4():
    test_contact = Contact.Contact( 'jfj',None,'top')
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db')
    assert db.add_contact(test_contact) == False

def test_contact_5():
    test_contact = Contact.Contact( None, 'jfj','top')
    db = DatabaseConnection.DatabaseConnection.get_connection('test_db')
    assert db.add_contact(test_contact) == False
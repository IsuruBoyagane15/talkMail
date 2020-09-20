import sqlite3


class DatabaseConnection:
    # define static instance to keep singleton DatabaseConnection object
    __instance = None

    # static method to get DatabaseConnection instance
    @staticmethod
    def get_connection(db_name):
        if DatabaseConnection.__instance is None:
            DatabaseConnection(db_name)
        return DatabaseConnection.__instance

    # constructor
    def __init__(self, db_name):
        if DatabaseConnection.__instance is not None:
            raise Exception("A DB connection instance has been already created...!")
        else:
            self.connection = sqlite3.connect(db_name, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                                name text NOT NULL,
                                email_address text NOT NULL PRIMARY KEY ,
                                password password NOT NULL
                                )""")

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
                                keyword text PRIMARY KEY NOT NULL,
                                contact_name text NOT NULL,
                                contact_email_address text UNIQUE NOT NULL
                                )""")
            DatabaseConnection.__instance = self

    # Remove user table from database
    def drop_user_table(self):
        self.cursor.execute("DROP TABLE user")

    # add user to database
    def add_user(self,user):
        current_users = self.get_user()
        try:
            if len(current_users) == 0:
                with self.connection:
                    self.cursor.execute("INSERT INTO user VALUES (:name, :email_address, :password)",
                                        {'name': user.name, 'email_address': user.email_address, 'password': user.password})
                return True
            else:
                return False
        except:
            return False

    # get user from database
    def get_user(self):
        self.cursor.execute("SELECT * FROM user")
        return self.cursor.fetchall()

    # remove user from database
    def remove_user(self):
        try:
            self.cursor.execute("DELETE FROM user")
            self.connection.commit()
            return True
        except:
            return False

    # add contact to database
    def add_contact(self, contact):
        try:
            with self.connection:
                self.cursor.execute("INSERT INTO contacts VALUES (:keyword, :contact_name, :contact_email_address)",
                                    {'keyword': contact.keyword, 'contact_name': contact.name, 'contact_email_address': contact.email_address})
            return True
        except sqlite3.IntegrityError:
                return False

    # get contact from database
    def get_contact(self, keyword_entered):
        self.cursor.execute("SELECT contact_email_address FROM contacts WHERE keyword = ?;", (keyword_entered,))
        return self.cursor.fetchall()


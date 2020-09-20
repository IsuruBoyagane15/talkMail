class User:
    # define static instance to keep singleton User object
    __instance = None

    # static method to get User instance
    @staticmethod
    def get_user(name, email_address, password):
        if User.__instance is None:
            User(name, email_address, password)
        return User.__instance

    # constructor
    def __init__(self, name, email_address, password):
        if User.__instance is not None:
            raise Exception("An User instance has been already created...!")
        else:
            self.name = name
            self.email_address = email_address
            self.password = password
            User.__instance = self

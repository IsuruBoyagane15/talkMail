from GuiMain import GuiMain
from RuturningThread import ReturningThread
from User import User
from InterfaceSpeaker import InterfaceSpeaker
from InterfaceListener import InterfaceListener
from EmailHandler import EmailHandler
from DatabaseConnection import DatabaseConnection
from GuiSignIn import GuiSignIn
from Contact import Contact
from GuiAddContact import GuiAddContact
from GuiRead import GuiRead
from GuiSend import GuiSend
from KeyListener import KeyListener

from PyQt5 import QtWidgets
from cryptography.fernet import Fernet
import sys
import threading
import os

dirname = os.path.dirname(__file__)


class Application:
    # define static instance to keep sigleton Application object
    __instance = None

    # static method to get Application instance
    @staticmethod
    def get_application():
        if Application.__instance is None:
            Application()
        return Application.__instance

    # constructor
    def __init__(self):

        if Application.__instance is not None:
            raise Exception("An application is already instantiated...!")
        else:
            self.db_connection = DatabaseConnection.get_connection("talkMail_db")
            print("Database connection is established.")
            self.email_handler = EmailHandler.get_email_handler()
            self.key_listener = KeyListener.get_key_listener(self)
            self.gui_app = QtWidgets.QApplication(sys.argv)
            self.lock_object = threading.Lock()
            self.terminate_thread = None

            self.send_gui = None
            self.start_gui = None
            self.read_gui = None
            self.sign_in_gui = None
            self.user_interface = None
            self.user = None

            # identify the encryption key
            try:
                os.mkdir(os.path.join(dirname + '/talkMail'))
                key_file = os.path.join(dirname + "/talkMail/key.txt")
                file = open(key_file, 'wb')
                key = Fernet.generate_key()
                file.write(key)
                file.close()
                self.encryption_key = key

            except FileExistsError:
                key_file = os.path.join(dirname + "/talkMail/key.txt")
                with open(key_file, 'rb') as f:
                    encryption_key = f.read()
                self.encryption_key = encryption_key

            # get user instance by calling sign in
            try:
                self.sign_in()
            except IndexError:
                self.quit()

            print("Application is initiated.")
            Application.__instance = self

    # start the app
    def start(self):
        # start a thread to catch "esc" key event to trigger termination
        self.terminate_thread = ReturningThread(target=self.key_listener.listen_for_key, args=())
        self.terminate_thread.start()
        print("Press 'esc' key to quit the application.")
        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
        self.user_interface.communicate("Welcome, If you want to quit the application, press escape key anytime",
                                        "message_quit", False)
        # run starting GUI containing main menu
        self.start_gui = GuiMain(self)
        self.run_gui(self.start_gui)

    # sign in method to get user if exists or take credentials
    def sign_in(self):

        # take user from db if exists
        users = self.db_connection.get_user()
        if len(users) == 1:
            self.user = User.get_user(users[0][0], users[0][1], users[0][2])

        # take users credentials
        else:
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("You need to sign in first.", "no_user_msg", False)
            self.sign_in_gui = GuiSignIn(self)
            self.run_gui(self.sign_in_gui)
            if self.user is None:
                print("You should sign in to proceed.")
                self.quit()

    # send email using Email Handler
    def send_email_command(self, message):

        my_email = self.user.email_address
        cipher_suite = Fernet(self.encryption_key)
        my_password = cipher_suite.decrypt(self.user.password).decode("utf-8")

        success = self.email_handler.send_email(my_email, my_password, message, self.user.name)

        if success:
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            print("Email is successfully sent.")
            self.user_interface.communicate("E-mail is successfully sent.", "sending_success", False)
        else:
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            print("Email is not successfully sent.")
            self.user_interface.communicate("Sending email failed, Try again.", "sending_failure", False)
            self.send_gui = GuiSend(self)
            self.run_gui(self.send_gui)

    #  request from start GUI to start send GUI
    def send_email_request(self):
        self.send_gui = GuiSend(self)
        self.run_gui(self.send_gui)

    # request from start GUI to read email
    def read_email_request(self, mailbox_type):
        emails = self.email_handler.load_email(self.user.email_address, self.user.password, self.encryption_key,
                                               mailbox_type)
        # emails are there to read in the mailbox
        if type(emails) == list:
            print(mailbox_type + " is opening. Wait a moment...")
            self.read_gui = GuiRead(self, emails, mailbox_type)
            self.run_gui(self.read_gui)
            return True

        # no emails in the email box
        elif not emails:
            print(mailbox_type + " is empty.")
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("No emails to read in " + mailbox_type + ", Try again",
                                            "empty_mailbox", False)
            return False

        # no internet connection
        else:
            print("Error, Check the internet connection")
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("Error, Check the internet connection", "no_internet", False)
            return False

    # request from start GUI to add contact
    def add_contact_request(self):
        self.add_contact_gui = GuiAddContact(self)
        self.run_gui(self.add_contact_gui)

    # request from start GUI to sign out
    def sign_out_request(self):
        status = self.db_connection.remove_user()
        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
        if status:
            self.user_interface.communicate("Signed Out successfully", "sign_out_success", False)
            self.user = None
            print("Signed Out successfully")
            self.quit()
            return True
        else:
            self.user_interface.communicate("Sign Out Failure, try again", "sign_out_failure", False)
            print("Sign Out Failure")
        return False

    # verify user credentials using EmailHandler
    def submit_credentials(self, name, email_address, password):
        verification = self.email_handler.verify_user(email_address, password)

        # correct credentials
        if verification is True:
            cipher_suite = Fernet(self.encryption_key)
            encrypted_password = cipher_suite.encrypt(password.encode())
            new_user = User.get_user(name, email_address, encrypted_password)
            self.db_connection.add_user(new_user)
            self.user = new_user
            print("User signed in successfully.")

        # incorrect credentails
        elif verification is False:
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("Sign in failed, Try again", "login_failure", False)
            self.sign_in_gui = GuiSignIn(self)
            self.run_gui(self.sign_in_gui)
            print("User sign in failure.")

        # connection error
        else:
            print("Error, Check the internet connection")
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("Error, Check the internet connection", "no_internet", False)

    # save contact in the database
    def submit_contact(self, email_address, keyword, name):

        new_contact = Contact(name, email_address, keyword)
        adding = self.db_connection.add_contact(new_contact)
        if not adding:
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("The keyword is taken", "contact_adding_failure", False)
            print("Try another keyword.")
            self.run_gui(GuiAddContact(self))

    # get email address of a recipient
    def get_recipients(self, recipient_type):
        addresses = []

        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
        self.user_interface.communicate("Specify the key word of the " + recipient_type + " recipient.",
                                        "keyword_request", True)
        self.user_interface = InterfaceListener.get_listener(self.lock_object)
        response = self.user_interface.communicate()

        if not response:
            return self.get_recipients(recipient_type)

        # add FIRST ADDRESS to the addresses list if a keyword is in database
        elif self.db_connection.get_contact(response.lower()):
            first_address = self.db_connection.get_contact(response.lower())[0][0]
            addresses.append(first_address)

            while True:
                self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
                self.user_interface.communicate("Do you want to add more " + recipient_type + " recipients?",
                                                "more_recipients", True)
                self.user_interface = InterfaceListener.get_listener(self.lock_object)
                more_recipients = self.user_interface.communicate()

                if not more_recipients:
                    continue

                elif more_recipients == "yes":
                    self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
                    self.user_interface.communicate("Specify the key word of the " + recipient_type + "  recipient.",
                                                    "keyword_request", True)
                    self.user_interface = InterfaceListener.get_listener(self.lock_object)
                    keyword_more = self.user_interface.communicate()

                    if not keyword_more:
                        continue

                    elif self.db_connection.get_contact(keyword_more):
                        new_to_address = self.db_connection.get_contact(keyword_more)[0][0]
                        if new_to_address not in addresses:
                            addresses.append(new_to_address)
                        else:
                            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
                            self.user_interface.communicate("This email address is already added.", "duplicate_address",
                                                            False)
                            print("This email address is already added.")
                            continue
                    else:
                        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
                        self.user_interface.communicate("Your keyword does not match for any contact", "no_keyword",
                                                        False)
                        continue

                elif more_recipients == "no":

                    self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
                    self.user_interface.communicate(recipient_type + " Recipients you selected", "recipient_list", True)

                    for i in addresses:
                        self.user_interface.communicate(i, "recipients" + str(addresses.index(i)), True)

                    confirmation = self.confirm_current_task()
                    if confirmation == 'yes':
                        return addresses
                    elif confirmation == 'no':
                        return self.get_recipients(recipient_type)
                else:
                    continue

        # ask to resubmit keyword for FIRST address which is essential
        else:
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("Your keyword does not match for any contact", "no_keyword", False)
            return self.get_recipients(recipient_type)

    # call recursive method to get fields
    def get_field(self, field_type):
        current_field = ''
        return self.get_field_recursive(field_type, current_field)

    # recursive method to get fields
    def get_field_recursive(self, field_type, field):

        if field_type == 'closure':
            separator = '\n'
        else:
            separator = '. '

        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
        self.user_interface.communicate("Enter the " + field_type, "enter_" + field_type, True)
        self.user_interface = InterfaceListener.get_listener(self.lock_object)
        response = self.user_interface.communicate()

        if response:

            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate(field_type + " you entered is... " + field + separator + response,
                                            "enter_+ type" + "_re", True)
            answer = False
            while not answer:
                answer = self.confirm_current_task()

                if answer == 'yes':
                    field += response + separator
                    while True:
                        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
                        self.user_interface.communicate("Do you want to add more to " + field_type + "?",
                                                        "more_" + field_type, True)

                        self.user_interface = InterfaceListener.get_listener(self.lock_object)
                        answer2 = self.user_interface.communicate()

                        if answer2 == 'yes':
                            return self.get_field_recursive(field_type, field)
                        elif answer2 == 'no':
                            return field
                        else:
                            continue

                elif answer == 'no':
                    return self.get_field_recursive(field_type, field)
        else:
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate('Try again', "try again", False)
            return self.get_field_recursive(field_type, field)

    # take confirmation for a given input
    def confirm_current_task(self):
        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
        self.user_interface.communicate("Do you confirm?", "confirmation", False)
        self.user_interface = InterfaceListener.get_listener(self.lock_object)

        response = self.user_interface.communicate()
        if response == 'yes':
            return 'yes'

        elif response == "no":
            self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
            self.user_interface.communicate("Try again!", "try_again", False)
            return 'no'
        else:
            return self.confirm_current_task()

    # shoe given window object
    def run_gui(self, gui):
        gui.show()
        self.gui_app.exec_()

    # give instruction about a button focused
    def instruct(self, message_type):
        self.user_interface = InterfaceSpeaker.get_speaker(self.lock_object)
        instruction_thread = threading.Thread(target=self.speak, args=(message_type,))
        instruction_thread.start()
        del instruction_thread

    # speak the instruction
    def speak(self, message_type):
        if message_type == 'send':
            self.user_interface.communicate("Press space to start sending email, press tab otherwise",
                                            "instruction_send", False)
        elif message_type == 'inbox':
            self.user_interface.communicate("Press space to start reading recieved emails,  press tab otherwise",
                                            "instruction_inbox", False)
        elif message_type == 'contact':
            self.user_interface.communicate("Press space to start add a contact, press tab otherwise",
                                            "instruction_add_contact", False)
        elif message_type == 'sentbox':
            self.user_interface.communicate("Press space to start reading sent email , press tab otherwise",
                                            "instruction_sent_box", False)
        elif message_type == 'read_previous_email':
            self.user_interface.communicate("Press space to read previous email , press tab otherwise",
                                            "instruction_previous_email", False)
        elif message_type == 'read_next_email':
            self.user_interface.communicate("Press space to read next email, press tab otherwise",
                                            "instruction_next_email", False)
        elif message_type == 'finish_reading_email':
            self.user_interface.communicate("Press space to finish reading emails, press tab otherwise",
                                            "instruction_finish_reading", False)
        elif message_type == 'no_previous_emails':
            self.user_interface.communicate("No previous emails to read", "instruction_no_previous_emails", False)
        elif message_type == 'no_more_emails':
            self.user_interface.communicate("No more emails to read", "instruction_no_more_emails", False)
        elif message_type == 'missing_field':
            self.user_interface.communicate("You miss som fields to enter. Try again",
                                            "instruction_missing_field", False)
        elif message_type == 'confirm_termination':
            self.user_interface.communicate("Press escape again to confirm termination, otherwise press any other key.",
                                            "instruction_terminate", False)
        elif message_type == 'quit':
            self.user_interface.communicate("Press space to quit, press tab otherwise.", "instruction_quit", False)
        elif message_type == 'confirm_sending':
            self.user_interface.communicate("Press space to send email, press tab otherwise.",
                                            "instruction_send_confirm", False)
        elif message_type == 'duplicate_recipients':
            self.user_interface.communicate("There are duplicate recipients. Try again.",
                                            "instruction_duplicate_recipients", False)
        elif message_type == 'sign_out':
            self.user_interface.communicate("Press space to sign out and leave, press tab otherwise.",
                                            "instruction_sign_out", False)
        elif message_type == 'attach':
            self.user_interface.communicate("Press space to add attachment, press tab otherwise.",
                                            "instruction_attachment", False)
        elif message_type == 'to':
            self.user_interface.communicate("Press space to add recipients, press tab otherwise.",
                                            "instruction_to", False)
        elif message_type == 'cc':
            self.user_interface.communicate("Press space to add carbon copy recipients, press tab otherwise.",
                                            "instruction_cc", False)
        elif message_type == 'bcc':
            self.user_interface.communicate("Press space to add blind carbon copy recipients, press tab otherwise.",
                                            "instruction_bcc", False)
        elif message_type == 'subject':
            self.user_interface.communicate("Press space to add subject, press tab otherwise.",
                                            "instruction_subject", False)
        elif message_type == 'content':
            self.user_interface.communicate("Press space to add content, press tab otherwise.",
                                            "instruction_content", False)
        elif message_type == 'closure':
            self.user_interface.communicate("Press space to add closure, press tab otherwise.",
                                            "instruction_closure", False)
        elif message_type == 'illegal_address':
            self.user_interface.communicate("Email address entered is illegal, try again",
                                            "instruction_illegal_address", False)
        elif message_type == 'read_wait':
            self.user_interface.communicate("Email is loading... wait a minute.", "instruction_read_waiting", False)
        elif message_type == 'use_keyboard':
            self.user_interface.communicate("Try using keyboard inputs.", "instruction_use_keyboard", False)
        else:
            self.user_interface.communicate(message_type, "email_text", True)

    # close the app
    def quit(self):
        print("Application is closing...!")
        os._exit(0)


# execution point
if __name__ == "__main__":
    app = Application.get_application()
    app.start()

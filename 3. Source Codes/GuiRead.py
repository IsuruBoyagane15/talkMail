from Gui import Gui

import os
from PyQt5 import QtCore, QtWidgets


dirname = os.path.dirname(__file__)


class GuiRead(Gui):
    def __init__(self, main, email_list, mailbox):
        super(GuiRead, self).__init__(main)
        self.setWindowTitle("Read " + mailbox)
        self.setMinimumSize(QtCore.QSize(620, 660))
        # style overriding
        self.setStyleSheet("""
                                                            #window {
                                                                background-color: #282827;
                                                            }
                                                            .QPlainTextEdit {
                                                                background-color:#c9c9c9;
                                                                color: black;
                                                                font : 10pt Courier New;
                                                            }

                                                            .QPushButton{
                                                            background-color : #444444;
                                                            color : #E25D33;
                                                            font : 14pt Courier New;

                                                            border-style: outset;
                                                            border-width: 1px;
                                                            border-radius: 8px;
                                                            border-color: #E25D33;
                                                            padding: 4px;
                                                            }
                                                            """)

        self.email_list = email_list
        self.mailbox = mailbox
        self.current_email_index = 0

        # widget containing email text
        self.email_text = QtWidgets.QPlainTextEdit(self)
        self.email_text.insertPlainText(self.format_email(self.email_list[self.current_email_index]))
        self.email_text.setReadOnly(True)

        self.email_text.move(20, 20)
        self.email_text.resize(580, 580)
        self.email_text.textChanged.connect(self.replace_text)

        # button to read previous emails
        self.button1 = QtWidgets.QPushButton('Previous Email', self)
        self.button1.move(20, 610)
        self.button1.resize(180, 40)
        self.button1.clicked.connect(self.submit1)

        # button to read next emails
        self.button2 = QtWidgets.QPushButton('Next Email', self)
        self.button2.move(220, 610)
        self.button2.resize(180, 40)
        self.button2.clicked.connect(self.submit2)

        # button to finish
        self.button3 = QtWidgets.QPushButton('Finish', self)
        self.button3.move(420, 610)
        self.button3.resize(180, 40)
        self.button3.clicked.connect(self.close)

        # add widgets to event listener
        for item in (self.button1, self.button2, self.button3, self.email_text):
            item.installEventFilter(self)

    # process the focus event
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.FocusIn:
            if self.button1 is obj:
                self.main.instruct('read_previous_email')
            elif self.button2 is obj:
                self.main.instruct('read_next_email')
            elif self.button3 is obj:
                self.main.instruct('finish_reading_email')
            elif self.email_text is obj:
                self.main.instruct('read_wait')
                self.main.instruct(self.email_text.toPlainText())
                self.button1.setFocus()

        return super(GuiRead, self).eventFilter(obj, event)

    # display and read previous email
    def submit1(self):
        if self.current_email_index != 0:
            self.email_text.clear()
            self.current_email_index -= 1
            self.email_text.insertPlainText(self.format_email(self.email_list[self.current_email_index]))
        else:
            self.main.instruct('no_previous_emails')
            self.button2.setFocus()

    # display and read next email
    def submit2(self):
        if self.current_email_index != len(self.email_list)-1:
            self.email_text.clear()
            self.current_email_index += 1
            self.email_text.insertPlainText(self.format_email(self.email_list[self.current_email_index]))
        else:
            self.main.instruct('no_more_emails')
            self.button1.setFocus()

    # replace the text email
    def replace_text(self):
        if self.email_text.toPlainText() != '':
            self.email_text.setFocus()

    # format the email message to read and display
    def format_email(self, email_message):
        string_email = ''
        if self.mailbox == 'inbox':
            string_email += 'Email was sent by ' + email_message['from'] + '\n\n'
        elif self.mailbox == 'sentbox' and email_message['to'] is not None:
            string_email += 'Email was sent to ' + email_message['to'] + '\n\n'

        if email_message['cc'] is not None and email_message['cc'] != '':
            string_email += 'Carbon copy recipients are ' + email_message['cc'] + '\n\n'

        if self.mailbox == 'sentbox' and email_message['bcc'] is not None and email_message['bcc'] != '':
            string_email += 'Blind carbon copy recipients are ' + email_message['bcc'] + '\n\n'

        if email_message['subject'] is not None:
            string_email += 'Subject is ' + email_message['subject'] + '\n\n'
        else:
            string_email += 'No subject specified in this email.\n\n'

        if email_message['body'] is not None:
            string_email += 'Email content is  ' + email_message['body'] + '\n\n'
        else:
            string_email += 'No content specified in this email.\n\n'
        string_email += 'End of the email...'
        return string_email



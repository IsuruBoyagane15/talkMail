import sys

from Gui import Gui
from RuturningThread import ReturningThread

from PyQt5 import QtWidgets, QtCore
import threading
from pynput.keyboard import Listener, Key


class GuiSend(Gui):

    # constructor
    def __init__(self, main):
        super(GuiSend, self).__init__(main)
        self.setMinimumSize(QtCore.QSize(620, 660))
        self.setWindowTitle("Send Email")
        # overide styles
        self.setStyleSheet("""
                                                            #window {
                                                                background-color: #282827;
                                                            }
                                                            .QLineEdit {
                                                                background-color:#f7f7f7;
                                                                color: black;
                                                                font : 10pt Courier New;
                                                            }
                                                            .QTextEdit {
                                                                background-color:#f7f7f7;
                                                                color: black;
                                                                font : 10pt Courier New;
                                                            }
                                                            .QLabel{
                                                                color: #E25D33;
                                                                font : 12pt Courier New;
                                                            }
                                                            .QPushButton{
                                                            background-color : #282827;
                                                            color : #E25D33;
                                                            font : 16pt Courier New;
                                                            }
                                                            """)

        self.email_message = {}
        self.attachments = []
        self.thread = None
        self.thread_of_method = None

        # button to get to recipients
        self.button1 = QtWidgets.QPushButton("To", self)
        self.button1.move(50, 40)
        self.button1.resize(150, 24)
        self.button1.clicked.connect(self.submit1)

        # button to get cc recipients
        self.button2 = QtWidgets.QPushButton("Cc", self)
        self.button2.move(50, 80)
        self.button2.resize(150, 24)
        self.button2.clicked.connect(self.submit2)

        # button to get bcc recipients
        self.button3 = QtWidgets.QPushButton("Bcc", self)
        self.button3.move(50, 120)
        self.button3.resize(150, 24)
        self.button3.clicked.connect(self.submit3)

        # button to get subject
        self.button4 = QtWidgets.QPushButton("Subject", self)
        self.button4.move(50, 160)
        self.button4.resize(150, 24)
        self.button4.clicked.connect(self.submit4)

        # button to get content
        self.button5 = QtWidgets.QPushButton("Content", self)
        self.button5.move(50, 200)
        self.button5.resize(150, 24)
        self.button5.clicked.connect(self.submit5)

        # button to get closure
        self.button6 = QtWidgets.QPushButton("Closure", self)
        self.button6.move(50, 500)
        self.button6.resize(150, 24)
        self.button6.clicked.connect(self.submit6)

        # button to get attachments
        self.button7 = QtWidgets.QPushButton("Attachments", self)
        self.button7.move(50, 540)
        self.button7.resize(150, 24)
        self.button7.clicked.connect(self.submit7)
        self.button7.setObjectName('attachment_button')

        # button to send emails
        self.button8 = QtWidgets.QPushButton("Send Email", self)
        self.button8.move(90, 600)
        self.button8.resize(200, 40)
        self.button8.clicked.connect(self.submit8)

        # button to cancel
        self.button9 = QtWidgets.QPushButton("Cancel", self)
        self.button9.move(330, 600)
        self.button9.resize(200, 40)
        self.button9.clicked.connect(self.close)

        # textbox of to recipients inputs
        self.textbox1 = QtWidgets.QLineEdit(self)
        self.textbox1.move(210, 40)
        self.textbox1.resize(350, 24)

        # textbox of cc recipients inputs
        self.textbox2 = QtWidgets.QLineEdit(self)
        self.textbox2.move(210, 80)
        self.textbox2.resize(350, 24)

        # textbox of bcc recipients inputs
        self.textbox3 = QtWidgets.QLineEdit(self)
        self.textbox3.move(210, 120)
        self.textbox3.resize(350, 24)

        # textbox of to subject inputs
        self.textbox4 = QtWidgets.QLineEdit(self)
        self.textbox4.move(210, 160)
        self.textbox4.resize(350, 24)

        # textbox of to content inputs
        self.textbox5 = QtWidgets.QTextEdit(self)
        self.textbox5.move(210, 200)
        self.textbox5.resize(350, 280)

        # textbox of to closure inputs
        self.textbox6 = QtWidgets.QLineEdit(self)
        self.textbox6.move(210, 500)
        self.textbox6.resize(350, 24)

        # textbox of to attachment file names
        self.textbox7 = QtWidgets.QLineEdit(self)
        self.textbox7.move(210, 540)
        self.textbox7.resize(350, 24)

        # add buttons to event filter
        for item in (self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7,
                     self.button8, self.button9):
            item.installEventFilter(self)

    # process focus event
    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.FocusIn:
            if self.button1 is obj:
                self.main.instruct('to')

            elif self.button2 is obj:
                self.main.instruct('cc')

            elif self.button3 is obj:
                self.main.instruct('bcc')

            elif self.button4 is obj:
                self.main.instruct('subject')

            elif self.button5 is obj:
                self.main.instruct('content')

            elif self.button6 is obj:
                self.main.instruct('closure')

            elif self.button7 is obj:
                self.main.instruct('attach')

            elif self.button8 is obj:
                self.main.instruct('confirm_sending')

            elif self.button9 is obj:
                self.main.instruct('quit')

        return super(GuiSend, self).eventFilter(obj, event)

    # get to recipients
    def submit1(self):
        to_result = self.manage_inputs(self.main.get_recipients,'')
        self.listener.stop()

        if to_result is not None:
            to = ','.join(to_result)
            self.textbox1.clear()
            self.textbox1.insert(to)
            self.button2.setFocus()

    # get cc recipients
    def submit2(self):
        cc_result = self.manage_inputs(self.main.get_recipients,'carbon copy')
        self.listener.stop()
        if cc_result is not None:
            cc = ','.join(cc_result)
            self.textbox2.clear()
            self.textbox2.insert(cc)
            self.button3.setFocus()

    # get bcc recipients
    def submit3(self):
        bcc_result = self.manage_inputs(self.main.get_recipients,'blind carbon copy')
        self.listener.stop()
        if bcc_result is not None:
            bcc = ','.join(bcc_result)
            self.textbox3.clear()
            self.textbox3.insert(bcc)
            self.button4.setFocus()

    # get subject
    def submit4(self):
        subject_result = self.manage_inputs(self.main.get_field, 'subject')
        self.listener.stop()
        if subject_result is not None:
            self.textbox4.clear()
            self.textbox4.insert(subject_result)
            self.button5.setFocus()

    # get content
    def submit5(self):
        content_result = self.manage_inputs(self.main.get_field, 'content')
        self.listener.stop()
        if content_result is not None:
            self.textbox5.clear()
            self.textbox5.append(content_result)
            self.button6.setFocus()

    # get closure
    def submit6(self):
        closure_result = self.manage_inputs(self.main.get_field, 'closure')
        self.listener.stop()
        if closure_result is not None:
            self.textbox6.clear()
            self.textbox6.insert(closure_result)
            self.button7.setFocus()

    # open file system for attachments
    def submit7(self):
        file_open_dialog = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',)

        if file_open_dialog[0]:
            self.attachments.append(file_open_dialog[0])
            current = self.textbox7.text()
            self.textbox7.clear()
            self.textbox7.insert((current+','+(file_open_dialog[0].split('/')[-1]))[1:])
            self.button7.setFocus()

    # send email button
    def submit8(self):
        self.email_message['to'] = self.textbox1.text()
        self.email_message['cc'] = self.textbox2.text()
        self.email_message['bcc'] = self.textbox3.text()

        if self.email_message['to'] == '' and self.email_message['cc'] == '' and self.email_message['bcc'] == '':
            self.main.instruct('missing_field')

        else:
            recipients_list = self.email_message['to'].split(',') + self.email_message['cc'].split(',') + \
                              self.email_message['bcc'].split(',')
            temp = []
            for i in recipients_list:
                if i in temp and i != '':
                    self.main.instruct('duplicate_recipients')
                    break
                else:
                    temp.append(i)

            if temp == recipients_list:
                self.email_message['subject'] = self.textbox4.text()
                self.email_message['content'] = self.textbox5.toPlainText()
                self.email_message['closure'] = self.textbox6.text()
                self.email_message['attachments'] = self.attachments
                self.main.send_email_command(self.email_message)
                self.close()

    # run threads to get fields
    def manage_inputs(self, method_to_run, *arg):
        self.thread = ReturningThread(target=self.listen_for_key, args=())
        self.thread.start()
        self.thread_of_method = ReturningThread(target=method_to_run, args=(arg))
        self.thread_of_method.start()
        return self.thread_of_method.join()

    # key listener for terminate voice conversation
    def listen_for_key(self):
        with Listener(
                on_press=self.key_press) as self.listener:
            self.listener.join()

    # process key press event
    def key_press(self, key):
        if key == Key.end:
            self.main.lock_object.acquire()
            self.thread_of_method.raise_exception()
            # self.thread_of_method = None
            self.main.lock_object.release()
            print("Try using keyboard!")
            self.main.instruct('use_keyboard')
            sys.exit()


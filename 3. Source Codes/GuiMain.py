from PyQt5 import QtCore, QtWidgets, QtGui
import os
from functools import partial
from Gui import Gui

dirname = os.path.dirname(__file__)


class GuiMain(Gui):

    # constructor
    def __init__(self, main):
        super(GuiMain, self).__init__(main)
        self.setWindowTitle("talkMail")

        self.button1 = QtWidgets.QPushButton("Send Email", self)
        self.button2 = QtWidgets.QPushButton("Inbox", self)
        self.button3 = QtWidgets.QPushButton("Sent Box", self)
        self.button4 = QtWidgets.QPushButton("Add Contact", self)
        self.button5 = QtWidgets.QPushButton("Sign Out", self)
        self.button6 = QtWidgets.QPushButton("Quit", self)

        # add widgets to event listener
        for button in (self.button1, self.button2, self.button3, self.button4, self.button5, self.button6):
            button.installEventFilter(self)

        # styling image
        self.image = QtGui.QImage(os.path.join(dirname, "Data/mail.png"))
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(50, 20, 200, 200)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.label.setScaledContents(True)

        # send email button
        self.button1.move(50, 250)
        self.button1.resize(200, 40)
        self.button1.clicked.connect(partial(self.submit1, self.main))

        # read inbox button
        self.button2.move(50, 300)
        self.button2.resize(200, 40)
        self.button2.clicked.connect(partial(self.submit2, self.main))

        # read sentbox button
        self.button3.move(50, 350)
        self.button3.resize(200, 40)
        self.button3.clicked.connect(partial(self.submit3, self.main))

        # add contact button
        self.button4.move(50, 400)
        self.button4.resize(200, 40)
        self.button4.clicked.connect(partial(self.submit4, self.main))

        # sign out button
        self.button5.move(50, 450)
        self.button5.resize(200, 40)
        self.button5.clicked.connect(partial(self.submit5, self.main))

        # quit button
        self.button6.move(50, 500)
        self.button6.resize(200, 40)
        self.button6.clicked.connect(self.close)

    # process focus events
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.FocusIn:
            if self.button1 is obj:
                self.main.instruct('send')
            elif self.button2 is obj:
                self.main.instruct('inbox')
            elif self.button3 is obj:
                self.main.instruct('sentbox')
            elif self.button4 is obj:
                self.main.instruct('contact')
            elif self.button5 is obj:
                self.main.instruct('sign_out')
            elif self.button6 is obj:
                self.main.instruct('quit')
        return super(GuiMain, self).eventFilter(obj, event)

    # request to send
    def submit1(self, main):
        main.send_email_request()

    # request to read inbox
    def submit2(self, main):
        status = main.read_email_request('inbox')
        if not status:
            self.button4.setFocus()

    # request to read sentbox
    def submit3(self, main):
        status = main.read_email_request('sentbox')
        if not status:
            self.button4.setFocus()

    # request to add contact
    def submit4(self, main):
        main.add_contact_request()

    # request to sign ost
    def submit5(self, main):
        status = main.sign_out_request()
        if status:
            self.close()
        else:
            self.button6.setFocus()

    # request to quit
    def closeEvent(self, event):
        self.close()
        self.main.quit()



import re

from PyQt5 import QtWidgets, QtGui
from functools import partial
from Gui import Gui
import os


dirname = os.path.dirname(__file__)


class GuiAddContact(Gui):
    def __init__(self, main):

        super(GuiAddContact, self).__init__(main)
        self.setWindowTitle("Add Contact")

        # styling image
        self.image = QtGui.QImage(os.path.join(dirname, "Data/contact.png"))
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(50, 20, 200, 200)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.label.setScaledContents(True)

        # email address label
        self.label1 = QtWidgets.QLabel("Email Address", self)
        self.label1.move(40, 255)

        # keyword label
        self.label2 = QtWidgets.QLabel("Keyword", self)
        self.label2.move(40, 325)

        # Name label
        self.label3 = QtWidgets.QLabel("Name", self)
        self.label3.move(40, 395)

        # email address textbox input
        self.textbox1 = QtWidgets.QLineEdit(self)
        self.textbox1.move(40, 280)
        self.textbox1.resize(220, 28)

        # keyword textbox input
        self.textbox2 = QtWidgets.QLineEdit(self)
        self.textbox2.move(40, 350)
        self.textbox2.resize(220, 28)

        # name textbox input
        self.textbox3 = QtWidgets.QLineEdit(self)
        self.textbox3.move(40, 420)
        self.textbox3.resize(220, 28)

        # button to submit
        self.button1 = QtWidgets.QPushButton("Add Contact", self)
        self.button1.move(50, 480)
        self.button1.resize(200, 40)
        self.button1.clicked.connect(partial(self.submit1,self.textbox1, self.textbox2, self.textbox3, self.main))

        # button to cancel
        self.button2 = QtWidgets.QPushButton("Cancel", self)
        self.button2.move(50, 530)
        self.button2.resize(200, 40)
        self.button2.clicked.connect(self.close)

    # method triggered by submit button
    def submit1(self, textbox1, textbox2, textbox3, main):
        email_address = textbox1.text()
        keyword = textbox2.text().lower()
        name = textbox3.text()
        regular_email = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if name == '' or keyword == '' or email_address == '':
            main.instruct('missing_field')

        # validate emails
        elif not regular_email.match(email_address):
            main.instruct('illegal_address')

        else:
            self.close()
            self.main.submit_contact(email_address, keyword, name)

from PyQt5 import QtWidgets, QtGui
import os
from functools import partial
from Gui import Gui

dirname = os.path.dirname(__file__)


class GuiSignIn(Gui):
    # constructor
    def __init__(self, main):
        super(GuiSignIn, self).__init__(main)
        self.setWindowTitle("Sign In")

        # styling button
        self.image = QtGui.QImage(os.path.join(dirname, "Data/sign_in.png"))
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(50, 20, 200, 200)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.label.setScaledContents(True)

        # label of name
        self.label1 = QtWidgets.QLabel("Name", self)
        self.label1.move(40,255)

        # label of email address
        self.label2 = QtWidgets.QLabel("Email Address", self)
        self.label2.move(40, 325)

        # label of password
        self.label3 = QtWidgets.QLabel("Password", self)
        self.label3.move(40, 395)

        # textbox of name input
        self.textbox1 = QtWidgets.QLineEdit(self)
        self.textbox1.move(40, 280)
        self.textbox1.resize(220, 28)

        # textbox of email address input
        self.textbox2 = QtWidgets.QLineEdit(self)
        self.textbox2.move(40, 350)
        self.textbox2.resize(220, 28)

        # textbox of password input
        self.textbox3 = QtWidgets.QLineEdit(self)
        self.textbox3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.textbox3.move(40, 420)
        self.textbox3.resize(220, 28)

        # button for sign in
        self.button1 = QtWidgets.QPushButton("Sign In", self)
        self.button1.move(50, 480)
        self.button1.resize(200, 40)
        self.button1.clicked.connect(partial(self.submit1, self.textbox1, self.textbox2, self.textbox3, self.main))

        # button for cancel
        self.button2 = QtWidgets.QPushButton("Cancel", self)
        self.button2.move(50, 530)
        self.button2.resize(200, 40)
        self.button2.clicked.connect(self.close)

    # submit credentials
    def submit1(self, textbox1, textbox2, textbox3, main):
        name = textbox1.text()
        email_address = textbox2.text()
        password = textbox3.text()
        if name == '' or password == '' or email_address == '':
            main.instruct('missing_field')
        else:
            main.submit_credentials(name, email_address, password)
            self.close()


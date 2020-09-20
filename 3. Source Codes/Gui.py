from PyQt5 import QtWidgets, QtGui
import os

dirname = os.path.dirname(__file__)


class Gui(QtWidgets.QWidget):
    # constructor
    def __init__(self, main):

        super(Gui, self).__init__()
        self.main = main
        self.setGeometry(500, 50, 300, 600)
        self.setObjectName('window')
        self.setWindowIcon(QtGui.QIcon(os.path.join(dirname, "Data/mail.png")))
        # apply styles
        self.setStyleSheet("""
                                                    #window {
                                                        background-color: #282827;
                                                    }
                                                    .QLineEdit {
                                                        background-color:#f7f7f7;
                                                        color: black;
                                                        font : 10pt Courier New;
                                                    }
                                                    .QLabel{
                                                        color: #E25D33;
                                                        font : 16pt Courier New;
                                                    }
                                                    .QPushButton{
                                                    background-color : #444444;
                                                    color : #E25D33;
                                                    font : 16pt Courier New;
            
                                                    border-style: outset;
                                                    border-width: 1px;
                                                    border-radius: 8px;
                                                    border-color: #E25D33;
                                                    padding: 4px;
                                                    }
                                                    """)

from PyQt5 import QtCore, QtGui, QtWidgets
from encrypters import *
import sys
import os


class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainIcon = QtGui.QIcon(resource_path("lib/icons/lock.png"))
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(720, 520)

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowIcon(self.mainIcon)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setWindowTitle("Message Cipher")
        self.setCentralWidget(self.centralwidget)

        # Initialize the main mode. "e" for encryption and "d" for decryption
        self.mode = "e"

        # initialize buttons for the two modes
        self.encryptModeButton = QtWidgets.QPushButton(self.centralwidget)
        self.encryptModeButton.setObjectName("encryptTab")
        self.encryptModeButton.setGeometry(QtCore.QRect(10, 10, 90, 30))
        self.encryptModeButton.setText("Encryption")
        self.encryptModeButton.setDown(True)
        self.encryptModeButton.clicked.connect(lambda: self.functionSelection(self.encryptModeButton.objectName()))

        self.decryptModeButton = QtWidgets.QPushButton(self.centralwidget)
        self.decryptModeButton.setObjectName("decryptTab")
        self.decryptModeButton.setGeometry(QtCore.QRect(100, 10, 90, 30))
        self.decryptModeButton.setText("Decryption")
        self.decryptModeButton.clicked.connect(lambda: self.functionSelection(self.decryptModeButton.objectName()))

        # Add boxes for original message and encrypted message.
        self.message = QtWidgets.QTextEdit(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(10, 50, 700, 150))
        self.message.setObjectName("originalMessage")
        self.message.setAcceptDrops(True)

        self.ciphered_message = QtWidgets.QTextEdit(self.centralwidget)
        self.ciphered_message.setGeometry(QtCore.QRect(10, 360, 700, 150))
        self.ciphered_message.setObjectName("encryptedMessage")
        self.ciphered_message.setReadOnly(True)

        # Instantiate close and Minimize buttons
        self.closebtn = QtWidgets.QPushButton(self.centralwidget)
        self.closebtn.setGeometry(QtCore.QRect(690, 0, 30, 30))
        self.closebtn.setObjectName("close")
        self.closebtn.setIcon(QtGui.QIcon(resource_path("lib/icons/close.png")))
        self.closebtn.clicked.connect(self.close)

        self.minimizebtn = QtWidgets.QPushButton(self.centralwidget)
        self.minimizebtn.setGeometry(QtCore.QRect(660, 0, 30, 30))
        self.minimizebtn.setObjectName("minimize")
        self.minimizebtn.setIcon(QtGui.QIcon(resource_path("lib/icons/min.ico")))
        self.minimizebtn.clicked.connect(self.minimize)

        # Adding a cipher button connected to the main cipher or decipher function, based on selection and mode.
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(600, 210, 100, 75))
        self.btn.setObjectName("cipherBtn")
        self.btn.setText("Encrypt\nMessage")
        self.btn.clicked.connect(self.cipherBtn)

        # Adding a comboBox with the cipher options, which is connected with the cipherSelection function.
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 210, 120, 40))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Select Cipher")
        self.comboBox.addItem("Caesar Cipher")
        self.comboBox.addItem("ROT 13")
        self.comboBox.addItem("Alberti Cipher")
        self.comboBox.addItem("Vigenere Cipher")
        self.comboBox.currentTextChanged.connect(self.cipherSelection)

        # Add the label that will show the information on each cipher type.
        self.descriptionLabel = QtWidgets.QLabel(self.centralwidget)
        self.descriptionLabel.setGeometry(QtCore.QRect(140, 210, 450, 90))
        self.descriptionLabel.setObjectName("description")
        self.descriptionLabel.setText("Here the description of the cipher will be displayed")
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignLeft)

        # add the boxes for the parameters and the label for their text.
        self.arg1 = QtWidgets.QTextEdit(self.centralwidget)
        self.arg1.setGeometry(QtCore.QRect(145, 320, 90, 30))
        self.arg1.setObjectName("arg1")
        self.arg1.setAlignment(QtCore.Qt.AlignCenter)
        self.arg1.hide()

        self.arg1Title = QtWidgets.QLabel(self.centralwidget)
        self.arg1Title.setGeometry(QtCore.QRect(10,320,120,30))
        self.arg1Title.setObjectName("arg1Label")
        self.arg1Title.hide()
        self.arg1Title.setAlignment(QtCore.Qt.AlignCenter)
        self.arg1Title.setWordWrap(True)

        self.arg2 = QtWidgets.QTextEdit(self.centralwidget)
        self.arg2.setGeometry(QtCore.QRect(380, 320, 90, 30))
        self.arg2.setObjectName("arg2")
        self.arg2.hide()

        self.arg2Title = QtWidgets.QLabel(self.centralwidget)
        self.arg2Title.setGeometry(QtCore.QRect(250,320,120,30))
        self.arg2Title.setObjectName("arg2Label")
        self.arg2Title.hide()
        self.arg2Title.setAlignment(QtCore.Qt.AlignCenter)
        self.arg2Title.setWordWrap(True)

        self.arg3 = QtWidgets.QTextEdit(self.centralwidget)
        self.arg3.setGeometry(QtCore.QRect(620, 320, 90, 30))
        self.arg3.setObjectName("arg3")
        self.arg3.hide()
        self.arg3.setAlignment(QtCore.Qt.AlignCenter)

        self.arg3Title = QtWidgets.QLabel(self.centralwidget)
        self.arg3Title.setGeometry(QtCore.QRect(485,320,120,30))
        self.arg3Title.setObjectName("arg3Label")
        self.arg3Title.setAlignment(QtCore.Qt.AlignCenter)
        self.arg3Title.setWordWrap(True)
        self.arg3Title.hide()

        # Add a list for the arguments for iteration
        self.arguments = [self.arg1, self.arg2, self.arg3]

        # Add error pop-up window
        self.errorPopup = QtWidgets.QMessageBox(self)
        self.errorPopup.setObjectName("error")
        self.errorPopup.setIcon(QtWidgets.QMessageBox.Icon.Information)
        self.errorPopup.setWindowIcon(QtGui.QIcon(resource_path("lib/icons/info.png")))
        self.errorPopup.setWindowTitle("Invalid parameter")


        # set focus on the message box
        self.message.setFocus()

        # Add a property for the position for move window support
        self.oldPos = self.pos()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.applyStyleSheet()

    def applyStyleSheet(self):
        with open(resource_path("lib/stylesheet.txt")) as ss:
            self.setStyleSheet(ss.read())

    def keyPressEvent(self, a0):
        if a0.key() == QtCore.Qt.Key.Key_Escape:
            self.close()

    def close(self):
        self.close()
        return

    def minimize(self):
        self.showMinimized()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData().hasText():
            a0 = a0.mimeData().text()
            a0.acceptProposedAction()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Encrypter", "Encrypter"))
        self.btn.setText(_translate("MainWindow", "Encrypt\nMessage"))
        self.descriptionLabel.setText(_translate("MainWindow",
                                    "Please select a Cipher and this box will provide a brief description of it."))

    def cipherSelection(self):
        if self.comboBox.currentText() == "Caesar Cipher":
            self.descriptionLabel.setText("a type of substitution cipher in which each letter in the plaintext " +
                                           "is replaced by a letter some fixed number of positions down the alphabet. "+
                                            "Please indicate in the box the number of positions to change. ")
            self.arg2.show()
            self.arg2.setText("1")
            self.arg2Title.show()
            self.arg2Title.setText("Shift:")
            self.arg1.hide()
            self.arg1Title.hide()
            self.arg3.hide()
            self.arg3Title.hide()

        elif self.comboBox.currentText() == "ROT 13":
            self.descriptionLabel.setText("ROT13 is a simple letter substitution cipher that replaces a letter with "+
             "the 13th letter after it in the alphabet. It has the same effect as a Caesar Cipher with 13 shifts.")
            self.arg1.hide()
            self.arg2.hide()
            self.arg3.hide()
            self.arg1Title.hide()
            self.arg2Title.hide()
            self.arg3Title.hide()

        elif self.comboBox.currentText() == "Alberti Cipher":
            self.descriptionLabel.setText("A type of polyalphabetic cipher that uses two concentric disks. The " +
            "inner ring rotates respect the outer ring changing the meaning for each letter based on the letter in " +
            "latter. The message is translated using lowercase characters for the message and uppercase for rotations "+
            "in the disk. \n by default, the order in the \"inner\" circle is vtrpnljhfdbacegikmoqsuwy")
            self.arg1.show()
            self.arg2.show()
            self.arg3.show()
            self.arg1.setText("a")
            self.arg2.setText("10")
            self.arg3.setText("20")
            self.arg1Title.show()
            self.arg1Title.setText("Index:")
            self.arg2Title.show()
            self.arg2Title.setText("Minimum letters before change:")
            self.arg3Title.show()
            self.arg3Title.setText("Maximum letters before change:")

        elif self.comboBox.currentText() == "Vigenere Cipher":
            self.descriptionLabel.setText("A type of polyalphabetic cipher in which the message is encrypted based on "
                            + "a second word, which for each letter changes the its position in the alphabet.")
            self.arg2.show()
            self.arg2.setText("a")
            self.arg2Title.setText("Keyword:")
            self.arg2Title.show()
            self.arg1.hide()
            self.arg3.hide()
            self.arg1Title.hide()
            self.arg3Title.hide()

        else:
            self.descriptionLabel.setText("Please select a Cipher and this box will provide a brief description of it.")
            self.arg1.hide()
            self.arg2.hide()
            self.arg3.hide()
            self.arg1Title.hide()
            self.arg2Title.hide()
            self.arg3Title.hide()

        self.descriptionLabel.setWordWrap(True)
        for arg in self.arguments:
            arg.setAlignment(QtCore.Qt.AlignCenter)


    def cipherBtn(self):
        message = self.message.toPlainText()
        arg1 = self.arg1.toPlainText()
        arg2 = self.arg2.toPlainText()
        arg3 = self.arg3.toPlainText()

        if self.comboBox.currentText() == "Caesar Cipher":
            if not arg2.isnumeric():
                self.errorPopup.setText("Please enter a valid number")
                self.errorPopup.show()
                return
            if self.mode == "e":
                self.ciphered_message.setText(caesar_cipher(message, int(arg2)))
            else:
                self.ciphered_message.setText(caesar_cipher(message, -int(arg2)))


        if self.comboBox.currentText() == "ROT 13":
            self.ciphered_message.setText(rot13(message))

        if self.comboBox.currentText() == "Alberti Cipher":
            if not (arg1.isalpha() and len(arg1)==1):
                self.errorPopup.setText("Please enter a valid index (Index should be a lowercase character).")
                self.errorPopup.show()
                return
            if not (arg2.isnumeric() or arg2.isnumeric()):
                self.errorPopup.setText("Please enter valid numbers for the second and third parameters.")
                self.errorPopup.show()
                return
            elif int(arg3) < int(arg2):
                self.errorPopup.setText("Please enter the lower bound of the random number of letters in the second parameter and the higher one in the third parameter.")
                self.errorPopup.show()
                return
            if self.mode == "e":
                self.ciphered_message.setText(alberti_cipher(message, arg1, int(arg2), int(arg3)))
            else:
                self.ciphered_message.setText(alberti_decipher(message,arg1))

        if self.comboBox.currentText() == "Vigenere Cipher":
            if not (arg2.isalpha() and arg2.count(" ") == 0):
                self.errorPopup.setText("Please enter a valid keyword as parameter (a valid keyword should be lowercase and must not have numbers or punctuation marks).")
                self.errorPopup.show()
                return
            if self.mode == "e":
                self.ciphered_message.setText(vigenere_cipher(message, arg2))
            else:
                self.ciphered_message.setText(vigenere_decipher(message, arg2))



    def functionSelection(self, mode):
        if mode == "encryptTab":
            self.btn.setText("Encrypt\nMessage")
            self.encryptModeButton.setDown(True)
            self.encryptModeButton.setStyleSheet("background-color: rgba(55,31,27,0.3)")
            self.decryptModeButton.setStyleSheet("background-color: rgba(250,250,250,0.3)")
            self.mode = "e"

        else:
            self.btn.setText("Decrypt\nMessage")
            self.decryptModeButton.setDown(True)
            self.decryptModeButton.setStyleSheet("background-color: rgba(55,31,27,0.3)")
            self.encryptModeButton.setStyleSheet("background-color: rgba(250,250,250,0.3)")
            self.mode = "d"

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)




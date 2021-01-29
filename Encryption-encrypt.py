# -*- coding: utf-8 -*-
"""
Example code for use of Public key encryption in Python with pyQT.

The following script is not intended as a full application, but just a demonstration of the technique. Firstly public and private 
encryption keys should be generated using script Encryption-keys.py - the public key should be located in the Encrypt folder and 
the private key in the Decrypt folder. In real work usage the public key is distributed to all computers for encrypting data using 
script Encryption-encrypt.py - the data is then transferred to the reading computer using any method, such as email or USB stick. 
Once on the reading computer the data can be decrypted using the private key and script Encryption-decrypt.py. So in summary the 
public key should be shared with all wishing to encrypt a message, but the private key should NEVER BE SHARED.

@date: 30 January 2021

This source code is provided by Richard J Smith 'as is' and 'with all faults'. The provider makes no 
representations or warranties of any kind concerning the safety, suitability, inaccuracies, 
typographical errors, or other harmful components of this software.
"""

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextCursor

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

from pathlib import Path
import pathlib

qtcreator_file = "Encryption_encrypt.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

encrypted =b'Test'
limit = 400 #limit for number of characters in input text box
        
class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.quitButton.clicked.connect(self.on_Quitclick)
        self.encryptButton.clicked.connect(self.on_encyptclick)
        self.saveButton.clicked.connect(self.on_saveclick)
        self.textEditIN.textChanged.connect(self.updatecounter)
        self.saveButton.setEnabled(False)
        self.textEditIN.setText('Type your message to be encypted here - limit is 400 characters')  
            
    def on_Quitclick(self): #Quit button has been pressed         
        self.close()

    def on_saveclick(self):
        print('Button save clicked')
        self.saveFileDialog()
        
    def on_encyptclick(self):
        print('Button encrypt clicked')
        file = pathlib.Path("Encrypt/publickey.pem")
        if file.exists ():   
            print ("key file exists")
            fd = open('Encrypt/publickey.pem', "rb")
            public_key = RSA.importKey(fd.read())
            fd.close()
            global encrypted
            msg = self.textEditIN.toPlainText()
            msgASbytes = str.encode(msg)
            encryptor = PKCS1_OAEP.new(public_key)
            encrypted = encryptor.encrypt(msgASbytes)
            print("Encrypted:", binascii.hexlify(encrypted))
            self.saveButton.setEnabled(True)
        else: #key file do not exist
            print ("key file does not exists")
            selfbuttonReply = QMessageBox.question(self, 'Key files does not exist', "Please use key generation script to make required key files", QMessageBox.Ok, QMessageBox.Ok)
        self.saveButton.repaint()  
              
    def saveFileDialog(self):
        global encrypted
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Encrypted Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            print(encrypted)
            if Path(fileName).suffix != ".txt":
                fileName += ".txt"
            f = open(fileName, "wb")
            f.write(encrypted)
            f.close()

    def updatecounter(self): 
        msg = self.textEditIN.toPlainText()
        global limit
        if len(msg)>limit:   
            print('Input testbox limit reached')
            TextData = msg[:limit]
            self.textEditIN.setText(TextData)  
            self.textEditIN.moveCursor(QTextCursor.End)
        msg = self.textEditIN.toPlainText()  
        self.wordcountlabel.setText(f"Characters remaining: {round(int(limit - len(msg)),0)} chars")    
           
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
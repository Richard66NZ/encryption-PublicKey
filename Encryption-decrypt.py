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
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import pathlib

qtcreator_file = "Encryption_decrypt.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

encrypted =b'Test'

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.quitButton.clicked.connect(self.on_Quitclick)
        self.decryptButton.clicked.connect(self.on_decyptclick)
        self.loadButton.clicked.connect(self.on_loadclick)
        self.decryptButton.setEnabled(False)
        self.textEditOUT.setText('Your message will be descrypted here')  
       
    def on_Quitclick(self): #Quit button has been pressed         
        self.close()

    def on_loadclick(self):
        print('Button load clicked')
        self.openFileNameDialog()
        self.decryptButton.setEnabled(True)

    def on_decyptclick(self):
        print('Button decrypt clicked')
        global encrypted
        file = pathlib.Path("Decrypt/privatekey.pem")
        if file.exists ():
            print ("key file exists")
            fd = open('Decrypt/privatekey.pem', "rb")
            private_key = RSA.importKey(fd.read())
            fd.close()
            decryptor = PKCS1_OAEP.new(private_key)
            decrypted = decryptor.decrypt(encrypted)
            print('Decrypted:', decrypted)  
            my_decoded_str = decrypted.decode()
            self.textEditOUT.setText(my_decoded_str)
        else: #key file do not exist
            print ("key file does not exists")
            selfbuttonReply = QMessageBox.question(self, 'Key files does not exist', "Please use key generation script to make required key files", QMessageBox.Yes, QMessageBox.Yes)
        self.decryptButton.repaint()          
        
    def openFileNameDialog(self):
        global encrypted
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Encrypted Files (*.txt)", options=options)
        if fileName:
            print(fileName)            
            f = open(fileName, "rb")
            contents =f.read()
            print (contents)
            encrypted = contents
            self.decryptButton.repaint()   
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
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
#from Crypto.Cipher import PKCS1_OAEP

import pathlib

qtcreator_file = "Encryption_keys.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.quitButton.clicked.connect(self.on_Quitclick)
        self.makekeyButton.clicked.connect(self.on_makekey)
            
    def on_Quitclick(self): #Quit button has been pressed         
        self.close()

    def on_makekey(self):
        print('Button makekey clicked')
        #check if files already exist.
        file = pathlib.Path("Decrypt/privatekey.pem")
        if file.exists ():
            print ("key file already exist")

            buttonReply = QMessageBox.question(self, 'Key files already exist', "Do you wish to overwrite current keys?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes: #files already exist but overwrite
                print('Overwrite keys')
                self.makekeyButton.setEnabled(False)
                self.makekeyButton.update()  
                write_Key()
                self.makekeyButton.setEnabled(True)   
            else: #files exist so don't overwrite
                print('Cancel generate keys')

        else: #files do not exist so go ahead and generate key
            print ("key file does not exist")
            self.makekeyButton.setEnabled(False)
            self.makekeyButton.update()  
            write_Key()
            self.makekeyButton.setEnabled(True)    

def write_Key():
    #Generate a public/ private key pair using 4096 bits key length (512 bytes)
    new_key = RSA.generate(4096, e=65537)

    #The private key in PEM format
    private_key = new_key.exportKey("PEM")

    #The public key in PEM Format
    public_key = new_key.publickey().exportKey("PEM")

    print (private_key)
    fd = open("Decrypt/privatekey.pem", "wb")
    fd.write(private_key)
    fd.close()

    print (public_key)
    fd = open("Encrypt/publickey.pem", "wb")
    fd.write(public_key)
    fd.close()        
    print('Keys generated')               

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

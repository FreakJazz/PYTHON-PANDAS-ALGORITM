# qt5_ex.py

import sys
from PyQt5.QtWidgets import (
        QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFrame, QMessageBox
    )
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication
import paho.mqtt.client as mqtt    # Connect with the MQTT Library

class Principal(QWidget):
    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        self.title = title
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 320
        self.toogle = True
        self.view()

    def view(self):
        # window setup
        self.setWindowTitle(self.title)
#         self.setFixedWidth(self.width)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        ## use above line or below
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        
        # Variables
        self.keepalive = 60;
        self.clientid = "clientId-8w7ewY8ukX";
        
        # add label
        self.lbTitle = QLabel("Fixed width", self, text="Configurar MQTT")
        # margin: left, top; width, height
        self.lbTitle.setGeometry(QRect(100, 0, 600, 50))
        self.lbTitle.setWordWrap(True) # allow word-wrap
        # line_edit value will be displayed on label
        # add label PORT
        self.lbHost = QLabel("Fixed width", self, text="Host:")
        # margin: left, top; width, height
        self.lbHost .setGeometry(QRect(20, 50, 600, 50))
        self.lbHost .setWordWrap(True) # allow word-wrap

        # add edit PORT
        self.frame2 = QFrame(self)
        self.frame2.setGeometry(QRect(120, 50, 400, 50))
        # create line edit box
        self.leHost = QLineEdit(self.frame2)
        self.leHost.move(0,0)
        self.leHost.setText


        
        # add label PORT
        self.lbPort = QLabel("Fixed width", self, text="Port:")
        # margin: left, top; width, height
        self.lbPort.setGeometry(QRect(20, 80, 600, 50))
        self.lbPort.setWordWrap(True) # allow word-wrap

        # add edit PORT
        self.frame2 = QFrame(self)
        self.frame2.setGeometry(QRect(120, 80, 400, 50))
        # create line edit box
        self.lePort = QLineEdit(self.frame2)
        self.lePort.move(0,0)

        # add label USERNAME
        self.lbUsername = QLabel("Fixed width", self, text="Username:")
        # margin: left, top; width, height
        self.lbUsername.setGeometry(QRect(20, 110, 600, 50))
        self.lbUsername.setWordWrap(True) # allow word-wrap
        
        # add edit USERNAME
        self.frame3 = QFrame(self)
        self.frame3.setGeometry(QRect(120, 110, 400, 50))
        # create line edit box
        self.leUsername = QLineEdit(self.frame3)
        self.leUsername.move(0,0)
        
        # add label PASSWORD
        self.lbPassword = QLabel("Fixed width", self, text="Password:")
        # margin: left, top; width, height
        self.lbPassword.setGeometry(QRect(20, 140, 600, 50))
        self.lbPassword.setWordWrap(True) # allow word-wrap
        
        # add edit PASSWORD
        self.frame4 = QFrame(self)
        self.frame4.setGeometry(QRect(120, 140, 400, 50))
        # create line edit box
        self.lePassword = QLineEdit(self.frame4)
        self.lePassword.move(0,0)
        
        # add label topic
        self.lbTopic = QLabel("Fixed width", self, text="Topic:")
        # margin: left, top; width, height
        self.lbTopic.setGeometry(QRect(20, 170, 600, 50))
        self.lbTopic.setWordWrap(True) # allow word-wrap
        
        # add edit topic
        self.frame5 = QFrame(self)
        self.frame5.setGeometry(QRect(120, 170, 400, 50))
        # create line edit box
        self.leTopic = QLineEdit(self.frame5)
        self.leTopic.move(0,0)
        
        # add button
        self.btnConnect = QPushButton(self, text="Conectar")
        self.btnConnect.setToolTip("Change value of label")
        self.btnConnect.move(120, 220)
        self.btnConnect.clicked.connect(self.connect_mqtt)

        # add label topic
        self.lbState = QLabel("Fixed width", self, text="Desconectado")
        # margin: left, top; width, height
        self.lbState.setGeometry(QRect(20, 250, 600, 50))
        self.lbState.setWordWrap(True) # allow word-wrap

        # add button
        self.btnSend = QPushButton(self, text="Enviar")
        self.btnSend.setToolTip("Change value of label")
        self.btnSend.move(120, 260)
        self.btnSend.clicked.connect(self.send_data)

        self.show()

    @pyqtSlot()
    def send_data(self):
        self.client.publish(self.topic, 'hola')

    @pyqtSlot()
    def connect_mqtt(self):
        
        ##### para conectar mqtt y enviar el dato ####
        if self.toogle == True:
            self.host = self.leHost.text()
            self.port = self.lePort.text()
            self.username = self.leUsername.text()
            self.password = self.lePassword.text()
            self.topic = self.leTopic.text()

            if self.username == "" or self.password == "" or self.host == "" or self.port == "" or self.topic == "":
                QMessageBox.warning(self, "Advertencia", "Existen campos vacios")
            else:
                ##### FUNCTION PRINCIPAL #####
                self.client = mqtt.Client()     # Client Identifier
                self.client.on_connect = self.on_connect      # Conecction Function 
                self.client.on_message = self.on_message      # Message Function
                self.port = int( self.port)
                self.client.connect(self.host, self.port, self.keepalive)     # Host, terminal, keep alive
                self.client.username_pw_set(self.username,self.password)    # Username and Password
                #client.loop_forever()
                self.client.loop()
                self.lbState.setText("Contectado")
                self.btnConnect.setText("Desconectar")
                self.leHost.setDisabled(True)
                self.lePort.setDisabled(True)
                self.leUsername.setDisabled(True)
                self.lePassword.setDisabled(True)
                self.leTopic.setDisabled(True)
                self.toogle = False
        #### para desconectar y cerrar la otra ventana ####
        else:
            self.client.disconnect()
            self.leHost.setEnabled(True)
            self.lePort.setEnabled(True)
            self.leUsername.setEnabled(True)
            self.lePassword.setEnabled(True)
            self.leTopic.setEnabled(True)
            self.toogle = True
            self.btnConnect.setText("Desconectar")
            self.lbState.setText("Contectado")
            
    ####### FUNCTION ON CONNECT ######
    def on_connect(self,client, userdata, flags, rc):
        print('Connected(%s)',self.client._client_id)
        client.subscribe(self.topic, qos=0) 
        client.publish(self.topic,'Se establecio la conexion')

    ####### FUNCTION ON MESSAGE ######
    def on_message(self,client, userdata, message):
        print('----------------------')
        print('topic: %s',  message.topic)
        print('payload: %s', message.payload)
        print('qos: %d', message.qos)
        print(message.payload.decode("utf-8"))

def main():
    app = QApplication(sys.argv)
    w = Principal(title="MQTT CONFIG")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

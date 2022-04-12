# qt5_ex.py

import sys
from PyQt5.QtWidgets import (
        QMainWindow, QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFrame, QMessageBox
    )
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication
import paho.mqtt.client as mqtt    # Connect with the MQTT Library
from datetime import time
from os import error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from smbus import SMBus
import time
from bluetooth import *
from openpyxl import load_workbook
from analize import Ui_MainWindow

# host: 'b44eefb2cd114616914f947cbfe39ee5.s1.eu.hivemq.cloud',
# tls: true,
# port: 8883,
# clientId: 'your_client_id',
# auth: true,
# user: 'test29',
# pass: 'Test2903',
# channel: '/review_connection',


# Application Class
class Application(QMainWindow):
    #Método constructor de la clase
    def __init__(self, parent = None):
        #QMainWindow Start
        QMainWindow.__init__(self,parent)
        #Charge MainWindow 
#         uic.loadUi("analize.ui", self)
        self.view_mqtt = MQTT(title="MQTT CONFIG")
        self.view_mqtt.show()
        uic.loadUi("analize.ui", self)
        #Title
        self.setWindowTitle("ANALISIS")
        self.period = 0.01
        self.initial = 0
        self.final = 200
        self.bus = SMBus(1)
        self.address = 0x40
        print('clase', self.view_mqtt)
        
        self.bt_analize.clicked.connect(self.fn_analize)
        self.type.currentIndexChanged.connect(self.selectionchange)
        self.data.currentIndexChanged.connect(self.selectionchange1)
    
    def selectionchange1(self,i):
        print ("Items in the list are :")
		
        for count in range(self.data.count()):
            print (self.data.itemText(count))
        print ("Current index",i,"selection changed ",self.data.currentText())
		

    def selectionchange(self,i):
        print ("Items in the list are :")
		
        for count in range(self.type.count()):
            print (self.type.itemText(count))
        print ("Current index",i,"selection changed ",self.type.currentText())
		
    def fn_analize(self):
        self.result.setText("Analizando...")
        self.get_data = self.data.currentText()
        print(self.get_data)
        self.get_type = self.type.currentText()
        print(self.get_type)
        

        if self.get_data == "Datos" and self.get_type == "Barras Rotas":

            self.fn_barras_rotas()
        
        elif self.get_data == "Datos" and self.get_type == "Cortocircuito":

            self.fn_cortocircuito()

        elif self.get_data == "Tiempo real" and self.get_type == "Barras Rotas":
    
            self.fn_barras_rotas_real()

        elif self.get_data == "Tiempo real" and self.get_type == "Cortocircuito":
        
            self.fn_cortocircuito_real()

        else: 
            print("entro aca")

    def fn_barras_rotas(self):

        self.frecuencia = pd.read_excel('no_falla_frecuencia.xlsx', sheet_name = ['data'], engine = 'openpyxl')
        self.df_nffrec = self.frecuencia['data']
        self.fail_frec = self.df_nffrec['F_FRECUENCIA']
        self.fail_frec = self.fail_frec.to_numpy()
        self.nfail_frec = self.df_nffrec['NF_FRECUENCIA']
        self.nfail_frec = self.nfail_frec.to_numpy()
        self.time = self.df_nffrec['TIEMPO']
        self.time = self.time.to_numpy()
        self.test = self.df_nffrec['test']
        self.test = self.test.to_numpy()
        self.comp_fail = []
        self.comp_nfail = []
        self.comp_error = []
        self.time1 = []
        print(self.nfail_frec)
        
        for x in range(0,len(self.nfail_frec)):
            if self.fail_frec[x] > self.nfail_frec[x]:
                self.comp_fail.append(self.fail_frec[x])
                self.comp_nfail.append(self.nfail_frec[x])
                self.time1.append(self.time[x])
                
        for x in range(0,len(self.comp_fail)):

            self.comp_error.append(self.comp_fail[x]-self.comp_nfail[x])

        self.error_frec = self.nfail_frec - self.fail_frec
        self.s_error_frec = np.fft.fft(self.error_frec)

        self.falla = np.fft.fft(self.fail_frec)
        self.n_falla = np.fft.fft(self.nfail_frec)

        fig, ax = plt.subplots(3)

        ax[0].plot(self.time1, self.comp_fail,  color = 'blue')
        ax[0].plot(self.time1, self.comp_nfail,  color = 'red')
        plt.title('Grafica de la comparacion de fallas')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')

        ax[1].plot(self.time1, self.comp_error, color = 'blue')
        plt.title('GRAFICA ERROR Comparacion')

        ax[2].plot(self.time, self.falla,  color = 'blue')
        ax[2].plot(self.time, self.n_falla,  color = 'red')
        plt.title('Grafica de la comparacion de fallas')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        if self.falla.min()< self.n_falla.min():
            print("EXISTE FALLA BARRAS ROTAS")
            self.result.setText("EXISTE FALLA BARRAS ROTAS")
            self.view_mqtt.send_mqtt('FALLA BARRAS ROTAS', self.view_mqtt.topic)

        else:
            print("NO EXISTE FALLA")
            self.result.setText("NO EXISTE FALLA")
            self.view_mqtt.send_mqtt('NO EXISTE FALLA', self.view_mqtt.topic)

            

        # self.ff_s = np.sin(90 * 2 * np.pi * self.fail_frec) + 0.5 * np.sin(90 * 2 * np.pi * self.fail_frec)
        # self.nff_s = np.sin(90 * 2 * np.pi * self.nfail_frec) + 0.5 * np.sin(90 * 2 * np.pi * self.nfail_frec)
        
        # plt.plot(self.time[self.initial:self.final], self.test[self.initial:self.final], color = 'green')
        # plt.title('GRAFICA test AMPLITUD')
        # plt.show()
        # plt.plot(self.time[self.initial:self.final], self.error_frec[self.initial:self.final], color = 'green')
        # plt.title('GRAFICA ERROR FRECUENCIA')
        # plt.show()
        # plt.plot(self.time[self.initial:self.final], self.s_error_frec[self.initial:self.final], color = 'green')
        # plt.title('GRAFICA SEG_TRASNS ERROR FRECUENCIA')
        # plt.show()
        # plt.plot(self.time[self.initial:self.final], self.ff_s[self.initial:self.final], color = 'blue')
        # plt.title('GRAFICA TRA_FALLA FRECUENCIA')
        # plt.xlabel('FRECUENCY')
        # plt.ylabel('ESPECTRO [DB]')
        # plt.show()
        # plt.plot(self.time[self.initial:self.final], self.nff_s[self.initial:self.final], color = 'red')
        # plt.title('GRAFICA TRA_SIN_FALLA FRECUENCIA')
        # plt.xlabel('FRECUENCY')
        # plt.ylabel('')
        # plt.show()

    def fn_cortocircuito(self):

        self.df_corto_circuito = pd.read_csv('cortocircuito1.CSV')
        self.df_motor_sano = pd.read_csv('motor_sano.CSV')
        self.tiempo = np.linspace(0, 20, num = 1000)

        self.fail_cc = self.df_corto_circuito['Data1']
        self.fail_cc = self.fail_cc.to_numpy()
        self.fail_ms = self.df_motor_sano['Data1']
        self.fail_ms = self.fail_ms.to_numpy()

        self.fail_cc1 = []
        self.fail_ms1 = []

        for x in range(0, len(self.fail_ms)):
            self.fail_cc1.append(self.fail_cc[x]+20)
            self.fail_ms1.append(self.fail_ms[x]+25)
        
        self.corto = np.fft.fft(self.fail_cc1)
        self.sano = np.fft.fft(self.fail_ms1)
        print(self.corto.min(), self.sano.min())

        self.comp_corto = []
        self.comp_sano1 = []
        self.comp_error1 = []
        self.time1 = []
        self.comp_corto = []

        for x in range(0,len(self.fail_ms)):
            if self.corto[x] > self.sano[x]:
                self.comp_corto.append(self.corto[x])
                self.comp_sano1.append(self.sano[x])
                self.time1.append(self.tiempo[x])

        # ax[0].plot(self.tiempo[self.initial:self.final], self.fail_cc[self.initial:self.final],  color = 'blue')
        # ax[0].plot(self.tiempo[self.initial:self.final], self.fail_ms[self.initial:self.final],  color = 'green')
        # plt.title('GRAFICA FALLAS')
        # plt.xlabel('TIME')
        # plt.ylabel('AMPLITUDE')
        # plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')
        # plt.show()

        fig, ax = plt.subplots(3)
        ax[0].plot(self.tiempo[self.initial:self.final], self.fail_cc1[self.initial:self.final],  color = 'blue')
        ax[0].plot(self.tiempo[self.initial:self.final], self.fail_ms1[self.initial:self.final],  color = 'green')
        plt.title('GRAFICA FALLAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')

        ax[1].plot(self.time1[self.initial:self.final], self.comp_corto[self.initial:self.final],  color = 'blue')
        ax[1].plot(self.time1[self.initial:self.final], self.comp_sano1[self.initial:self.final],  color = 'green')
        plt.title('GRAFICA FALLAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')

        ax[2].plot(self.tiempo, self.corto,  color = 'blue')
        ax[2].plot(self.tiempo, self.sano,  color = 'red')
        plt.title('GRAFICA TRANSFORMADA CORTOCIRCUITO')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['CORTOCIRCUITO','MOTOR'], loc='upper right')
        plt.show()

        if self.corto.min() < self.sano.min():
            print("EXISTE FALLA CORTOCIRCUITO")
            self.result.setText("EXISTE FALLA CORTOCIRCUITO")
            self.view_mqtt.send_mqtt('FALLA CORTOCIRCUITO', self.view_mqtt.topic)
          
        else:
            print("NO EXISTE CORTOCIRCUITO")
            self.result.setText("NO EXISTE FALLA")
            self.view_mqtt.send_mqtt('NO EXISTE FALLA', self.view_mqtt.topic)

    def fn_barras_rotas_real(self):

        self.df_motor_sano = pd.read_csv('motor_sano.CSV')
        self.fail_ms = self.df_motor_sano['Data1']
        self.fail_ms = self.fail_ms.to_numpy()
        self.tiempo = np.linspace(0, 20, num = 1000) 
        self.fail_ms1 = []
        self.data_real = []

        self.comp_corto = []
        self.comp_sano1 = []
        self.time1 = []
        self.comp_corto = []
    
        for x in range(0, len(self.fail_ms)):
            self.fail_ms1.append(self.fail_ms[x]+25)
            self.get_data = self.fun_data()
            self.data_real.append(self.get_data)
            self.resp = self.fail_ms1[x]-self.data_real[x]
            print(self.get_data)
            time.sleep(self.period)

        for x in range(0,len(self.fail_ms)):
            if self.data_real[x] > self.fail_ms[x]:
                self.comp_corto.append(self.data_real[x])
                self.comp_sano1.append(self.fail_ms[x])
                self.time1.append(self.tiempo[x])

        self.falla = np.fft.fft(self.data_real)
        self.sano = np.fft.fft(self.fail_ms1)

        fig, ax = plt.subplots(3)
        ax[0].plot(self.tiempo[self.initial:self.final], self.data_real[self.initial:self.final],  color = 'blue')
        ax[0].plot(self.tiempo[self.initial:self.final], self.fail_ms1[self.initial:self.final],  color = 'green')
        plt.title('GRAFICA FALLAS BARRAS ROTAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')

        ax[1].plot(self.time1[self.initial:self.final], self.comp_corto[self.initial:self.final],  color = 'blue')
        ax[1].plot(self.time1[self.initial:self.final], self.comp_sano1[self.initial:self.final],  color = 'green')
        plt.title('GRAFICA FALLAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')

        ax[2].plot(self.tiempo, self.falla,  color = 'blue')
        ax[2].plot(self.tiempo, self.sano,  color = 'red')
        plt.title('GRAFICA TRANSFORMADA BARRAS ROTAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['CORTOCIRCUITO','MOTOR'], loc='upper right')
        plt.show()

        if self.falla.min() < self.sano.min():
            print("EXISTE FALLA BARRAS ROTAS")
            self.result.setText("EXISTE FALLA BARRAS ROTAS")
            self.mqtt.client.publish(self.mqtt.topic, 'FALLA BARRAS ROTAS')

        else:
            print("NO EXISTE BARRAS ROTAS")
            self.result.setText("NO EXISTE FALLA BARRAS ROTAS")
            self.view_mqtt.send_mqtt('NO EXISTE FALLA', self.view_mqtt.topic)
        

    def fn_cortocircuito_real(self):

        self.df_motor_sano = pd.read_csv('motor_sano.CSV')
        self.fail_ms = self.df_motor_sano['Data1']
        self.fail_ms = self.fail_ms.to_numpy()
        self.tiempo = np.linspace(0, 20, num = 1000)
        self.fail_ms1 = []
        self.data_real = []

        self.comp_corto = []
        self.comp_sano1 = []
        self.time1 = []
        self.comp_corto = []
    
        for x in range(0, len(self.fail_ms)):
            self.fail_ms1.append(self.fail_ms[x]+25)
            self.data_real.append(self.fun_data())
            self.resp = self.fail_ms[x]-self.data_real[x]
            print(self.data_real[x])
            time.sleep(self.period)

        for x in range(0,len(self.fail_ms)):
            if self.data_real[x] > self.fail_ms[x]:
                self.comp_corto.append(self.data_real[x])
                self.comp_sano1.append(self.fail_ms[x])
                self.time1.append(self.tiempo[x])

        self.falla = np.fft.fft(self.data_real)
        self.sano = np.fft.fft(self.fail_ms1)

        fig, ax = plt.subplots(3)
        ax[0].plot(self.tiempo[self.initial:self.final], self.data_real[self.initial:self.final],  color = 'blue')
        ax[0].plot(self.tiempo[self.initial:self.final], self.fail_ms1[self.initial:self.final],  color = 'green')
        plt.title('GRAFICA FALLAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')

        ax[1].plot(self.time1[self.initial:self.final], self.comp_corto[self.initial:self.final],  color = 'blue')
        ax[1].plot(self.time1[self.initial:self.final], self.comp_sano1[self.initial:self.final],  color = 'green')
        plt.title('GRAFICA FALLAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')

        ax[2].plot(self.tiempo, self.falla,  color = 'blue')
        ax[2].plot(self.tiempo, self.sano,  color = 'red')
        plt.title('GRAFICA TRANSFORMADA CORTOCIRCUITO')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['CORTOCIRCUITO','MOTOR'], loc='upper right')
        plt.show()

        if self.falla.min() < self.sano.min():
            print("EXISTE FALLA CORTOCIRCUITO")
            self.view_mqtt.send_mqtt('FALLA CORTOCIRCUITO', self.view_mqtt.topic)
            self.result.setText("EXISTE FALLA CORTOCIRCUITO")
        else:
            print("NO EXISTE CORTOCIRCUITO")
            self.view_mqtt.send_mqtt('NO EXISTE FALLA', self.view_mqtt.topic)
            self.result.setText("NO EXISTE FALLA")
            
class MQTT(QMainWindow):
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
        self.leHost.setText("broker.mqttdashboard.com")
        
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
        self.lePort.setText("1883")

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
        self.leUsername.setText("raspberry")
        
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
        self.lePassword.setText("raspberry")
        
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
        self.leTopic.setText("motor")
        
        # add button
        self.btnConnect = QPushButton(self, text="   Conectar   ")
        self.btnConnect.setToolTip("Change value of label")
        self.btnConnect.move(120, 220)
        self.btnConnect.clicked.connect(self.connect_mqtt)

        # add label topic
        self.lbState = QLabel("Fixed width", self, text="Desconectado")
        # margin: left, top; width, height
        self.lbState.setGeometry(QRect(20, 250, 600, 50))
        self.lbState.setWordWrap(True) # allow word-wrap
        self.host = self.leHost.text()
        self.port = self.lePort.text()
        self.username = self.leUsername.text()
        self.password = self.lePassword.text()
        self.topic = self.leTopic.text()
        self.client = mqtt.Client()     # Client Identifier
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
            self.btnConnect.setText("Conectar")
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
        
    def send_mqtt(self, val, topic):
        
        self.val = val
        self.topic =topic
#         self.client.subscribe(self.topic, qos=0)
        self.client.publish(self.topic, self.val)
        print('Valor', self.val)
        print('Topic', self.topic)

def main():
    app = QApplication(sys.argv)
    program = Application()
    program.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


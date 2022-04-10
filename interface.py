import sys
import os 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QFileDialog
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
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

# Application Class
class Application(QMainWindow):
    #Método constructor de la clase
    def __init__(self, parent = None):
        #QMainWindow Start
        QMainWindow.__init__(self,parent)
        #Charge MainWindow 
        uic.loadUi("analize.ui", self)
        #Title
        self.setWindowTitle("ANALISIS")
        self.period = 0.01
        self.initial = 0
        self.final = 200
        self.bus = SMBus(1)
        self.address = 0x40
        self.config_bluetooth()
        
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
            self.rx_and_echo('a')
#             self.send_data('b')
            self.result.setText("EXISTE FALLA BARRAS ROTAS")

        else:
            print("NO EXISTE FALLA")
            self.rx_and_echo("NO EXISTE FALLA")
            self.rx_and_echo('d')
            self.send_data('d')
            self.result.setText("NO EXISTE FALLA")

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
#             self.send_data('a')
#             self.rx_and_echo("EXISTE FALLA CORTOCIRCUITO")
            
        else:
            print("NO EXISTE CORTOCIRCUITO")
            self.result.setText("NO EXISTE FALLA")
            self.send_data('d')
            self.rx_and_echo("NO EXISTE CORTOCIRCUITO")

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
#             self.send_data('b')
            self.rx_and_echo("EXISTE FALLA BARRAS ROTAS")
        else:
            print("NO EXISTE BARRAS ROTAS")
            self.result.setText("NO EXISTE FALLA BARRAS ROTAS")
#             self.send_data('d')
            self.rx_and_echo("NO EXISTE FALLA BARRAS ROTAS")
        

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
            self.rx_and_echo("EXISTE FALLA CORTOCIRCUITO")
            self.send_data('a')
            self.result.setText("EXISTE FALLA CORTOCIRCUITO")
        else:
            print("NO EXISTE CORTOCIRCUITO")
            self.rx_and_echo("NO EXISTE CORTOCIRCUITO")
#             self.send_data('d')
            self.result.setText("NO EXISTE FALLA")

    def fun_data(self):
        self.data1 = self.bus.read_byte_data(self.address, 1)
        return self.data1
    
    # funcion de entrada de dato analogo
    
    def send_data(self, data):
        self.data1 = self.bus.read_byte_data(self.address,data)
    
        return self.data1
    
    def input_and_send(self, data):
        self.addr = "E8:7F:6B:E1:B5:E0"
        self.service_matches = find_service( address = self.addr )

        self.buf_size = 1024;

        if len(self.service_matches) == 0:
            print("couldn't find the SampleServer service =(")
            sys.exit(0)

        for s in range(len(self.service_matches)):
            print("\nservice_matches: [" + str(s) + "]:")
            print(self.service_matches[s])
            
        self.first_match = self.service_matches[0]
        self.port = self.first_match["port"]
        self.name = self.first_match["name"]
        self.host = self.first_match["host"]

        self.port=2
        print("connecting to \"%s\" on %s, port %s" % (self.name, self.host, self.port))

        # Create the client socket
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect(self.host, self.port)
        print("connected")
    
    def config_bluetooth(self):
         
        self.addr = "E8:7F:6B:E1:B5:E0"
        self.service_matches = find_service( address = self.addr )
        self.buf_size = 1024;
            
        if len(self.service_matches) == 0:
            print("couldn't find the SampleServer service =(")
            sys.exit(0)

        for s in range(len(self.service_matches)):
            print("\nservice_matches: [" + str(s) + "]:")
            print(self.service_matches[s])
            
        self.first_match = self.service_matches[0]
        self.port = self.first_match["port"]
        self.name = self.first_match["name"]
        self.host = self.first_match["host"]

        self.port=2
        print("connecting to \"%s\" on %s, port %s" % (self.name, self.host, self.port))

        # Create the client socket
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((self.host, self.port))
        print("connected")
        
    def rx_and_echo(self,fail):
        self.sock.send(fail)
#         self.data = self.sock.recv(self.buf_size)
#             if self.data:
#                 print(self.data)
#                 self.sock.send(self.data)


if __name__ == "__main__": 
    app = QApplication(sys.argv)        #App Inicialization
    _Application = Application()        #Object Class
    _Application.show()                 #Show Window
    app.exec_()                         #Execute Aplication
    #sys.exit(app.exec_())
    
    
    
    
    
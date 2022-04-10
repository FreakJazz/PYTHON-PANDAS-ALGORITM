from datetime import time
from os import error
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Application Class
class DataAnalisys():
    #Método constructor de la clase
    def __init__(self, parent = None):
        initial = 0
        final = 1000
        count_corto = 0
        count_barras = 0

        df_barras_rotas = pd.read_csv('barras_rotas.CSV')
        df_corto_circuito = pd.read_csv('cortocircuito1.CSV')
        df_motor_sano = pd.read_csv('motor_sano.CSV')
        tiempo = np.linspace(0, 20, num = 1000)

        fail_br = df_barras_rotas['Data1']
        fail_br = fail_br.to_numpy()
        fail_cc = df_corto_circuito['Data1']
        fail_cc = fail_cc.to_numpy()
        fail_ms = df_motor_sano['Data1']
        fail_ms = fail_ms.to_numpy()

        plt.plot(tiempo[initial:final], fail_br[initial:final],  color = 'blue')
        plt.plot(tiempo[initial:final], fail_cc[initial:final],  color = 'red')
        plt.plot(tiempo[initial:final], fail_ms[initial:final],  color = 'green')
        plt.title('GRAFICA FALLAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')
        plt.show()
        
        fail_br1 = []
        fail_cc1 = []
        fail_ms1 = []

        for x in range(0, len(fail_ms)):
            fail_br1.append(fail_br[x]+25)
            fail_cc1.append(fail_cc[x]+20)
            fail_ms1.append(fail_ms[x]+25)

        plt.plot(tiempo[initial:final], fail_br1[initial:final],  color = 'blue')
        plt.plot(tiempo[initial:final], fail_cc1[initial:final],  color = 'red')
        plt.plot(tiempo[initial:final], fail_ms1[initial:final],  color = 'green')
        plt.title('GRAFICA FALLAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL_BR','FAIL_CC', 'NO FAIL'], loc='upper right')
        plt.show()

        barras = np.fft.fft(fail_br1)
        corto = np.fft.fft(fail_cc1)
        sano = np.fft.fft(fail_ms1)
        print(barras.min(), corto.min(), sano.min())


        comp_corto = []
        comp_sano1 = []
        comp_error1 = []
        time1 = []
        comp_corto = []
        comp_error1 = []

        for x in range(0,len(fail_ms)):
            if barras[x] > sano[x]:
                comp_corto.append(barras[x])
                comp_sano1.append(sano[x])
                
                time1.append(tiempo[x])
        # for x in range(0,len(comp_fail)):

        #     comp_error.append(comp_fail[x]-comp_nfail[x])    

        if barras.min() < sano.min():
            print("EXISTE FALLA BARRAS ROTAS")
        else:
            print("NO EXISTE FALLA BARRAS ROTAS")

        if corto.min() < sano.min():
            print("EXISTE FALLA CORTOCIRCUITO")
        else:
            print("NO EXISTE CORTOCIRCUITO")

        plt.plot(tiempo, barras,  color = 'blue')
        plt.plot(tiempo, sano,  color = 'red')
        plt.title('GRAFICA TRANSFORMADA BARRAS ROTAS')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['BARRAS ROTAS','MOTOR'], loc='upper right')
        plt.show()

        plt.plot(tiempo, corto,  color = 'blue')
        plt.plot(tiempo, sano,  color = 'red')
        plt.title('GRAFICA TRANSFORMADA CORTOCIRCUITO')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['CORTOCIRCUITO','MOTOR'], loc='upper right')
        plt.show()
        
        



if __name__ == "__main__": 
    app = DataAnalisys(None)
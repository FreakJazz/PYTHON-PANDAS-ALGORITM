from datetime import time
from os import error
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Application Class
class Data_analisys():
    #Método constructor de la clase
    def __init__(self, parent = None):
        initial = 0
        final = 200

        #########################################################
        #################### AMPLITUD ###########################
        #########################################################

        f_amplitude = pd.read_excel('falla_amplituddesf.xlsx', sheet_name = ['data'])
        df_famp = f_amplitude['data']
        print(df_famp)
        df_famp.plot(x = 'TIEMPO', y = 'F_AMPLITUD',  color = 'blue')
        df_famp.plot(x = 'TIEMPO', y = 'NF_AMPLITUD',  color = 'red')
        plt.title('GRAFICA AMPLITUD')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()
        
        fail_amp = df_famp['F_AMPLITUD']
        fail_amp = fail_amp.to_numpy()
        nfail_amp = df_famp['NF_AMPLITUD']
        nfail_amp = nfail_amp.to_numpy()
        time = df_famp['TIEMPO']
        time = time.to_numpy()

        plt.plot(time, fail_amp,  color = 'blue')
        plt.plot(time, nfail_amp,  color = 'red')
        plt.title('GRAFICA AMPLITUD COMPLETA')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        error = nfail_amp - fail_amp
        s_error = np.fft.fft(error)

        fa_s = np.sin(90 * 2 * np.pi * fail_amp) + 0.5 * np.sin(90 * 2 * np.pi * fail_amp)
        nfa_s = np.sin(90 * 2 * np.pi * nfail_amp) + 0.5 * np.sin(90 * 2 * np.pi * nfail_amp)

        plt.plot(time[initial:final], error[initial:final], color = 'green')
        plt.title('GRAFICA ERROR AMPLITUD')
        plt.show()
        
        plt.plot(time[initial:final], s_error[initial:final], color = 'green')
        plt.title('GRAFICA SEGUNDA_TRA ERROR AMPLITUD')
        plt.show()
        plt.plot(time[initial:final], fa_s[initial:final], color = 'blue')
        plt.title('GRAFICA TRA_FALLA AMPLITUD')
        plt.show()    
        plt.plot(time[initial:final], nfa_s[initial:final], color = 'red')
        plt.title('GRAFICA TRA_SIN_FALLA AMPLITUD')
        plt.show()

        falla = np.fft.fft(fail_amp)
        n_falla = np.fft.fft(nfail_amp)
        
        if falla.min() < n_falla.min():
            print("falla_max",falla.min(), "no falla max",n_falla.min())
            print("EXISTE FALLA")
        else:
            print("NO EXISTE FALLA")

        plt.plot(time[initial:final], falla[initial:final], color = 'green')
        plt.plot(time[initial:final], n_falla[initial:final], color = 'blue')
        plt.title('GRAFICA SEGUNDA TRANSFORMADA AMPLITUD')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        plt.plot(time[initial:final], fail_amp[initial:final], color = 'blue')
        plt.plot(time[initial:final], nfail_amp[initial:final], color = 'red')
        plt.title('GRAFICA COMPARACIÓN AMPLITUD')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        plt.scatter(time[initial:final], fail_amp[initial:final], color = 'blue')
        plt.scatter(time[initial:final], nfail_amp[initial:final], color = 'red')
        plt.title('GRAFICA VERIFICACIÓN AMPLITUD')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()
        
        #########################################################
        ################### FRECUENCIA ##########################
        #########################################################

        frecuencia = pd.read_excel('no_falla_frecuencia.xlsx', sheet_name = ['data'])
        df_nffrec = frecuencia['data']
        print(df_nffrec)
        fail_frec = df_nffrec['F_FRECUENCIA']
        fail_frec = fail_frec.to_numpy()
        nfail_frec = df_nffrec['NF_FRECUENCIA']
        nfail_frec = nfail_frec.to_numpy()
        time = df_nffrec['TIEMPO']
        time = time.to_numpy()
        test = df_nffrec['test']
        test = test.to_numpy()
        comp_fail = []
        comp_nfail = []
        comp_error = []
        time1 = []
        for x in range(0,len(nfail_frec)):
            if fail_frec[x] > nfail_frec[x]:
                comp_fail.append(fail_frec[x])
                comp_nfail.append(nfail_frec[x])
                time1.append(time[x])
        for x in range(0,len(comp_fail)):

            comp_error.append(comp_fail[x]-comp_nfail[x])      

        plt.plot(time1, comp_fail,  color = 'blue')
        plt.plot(time1, comp_nfail,  color = 'red')
        plt.title('Grafica de la comparacion de fallas')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()
        plt.plot(time1, comp_error, color = 'blue')
        plt.title('GRAFICA ERROR Comparacion')
        plt.show()

        plt.plot(time, fail_frec,  color = 'blue')
        plt.plot(time, nfail_frec,  color = 'red')
        plt.title('GRAFICA AMPLITUD COMPLETA')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        error_frec = nfail_frec - fail_frec
        s_error_frec = np.fft.fft(error_frec)

        ff_s = np.sin(90 * 2 * np.pi * fail_frec) + 0.5 * np.sin(90 * 2 * np.pi * fail_frec)
        nff_s = np.sin(90 * 2 * np.pi * nfail_frec) + 0.5 * np.sin(90 * 2 * np.pi * nfail_frec)
        
        plt.plot(time[initial:final], test[initial:final], color = 'green')
        plt.title('GRAFICA test AMPLITUD')
        plt.show()
        plt.plot(time[initial:final], error_frec[initial:final], color = 'green')
        plt.title('GRAFICA ERROR FRECUENCIA')
        plt.show()
        plt.plot(time[initial:final], s_error_frec[initial:final], color = 'green')
        plt.title('GRAFICA SEG_TRASNS ERROR FRECUENCIA')
        plt.show()
        plt.plot(time[initial:final], ff_s[initial:final], color = 'blue')
        plt.title('GRAFICA TRA_FALLA FRECUENCIA')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.show()    
        plt.plot(time[initial:final], nff_s[initial:final], color = 'red')
        plt.title('GRAFICA TRA_SIN_FALLA FRECUENCIA')
        plt.xlabel('FRECUENCY')
        plt.ylabel('')
        plt.show()

        falla = np.fft.fft(fail_frec)
        n_falla = np.fft.fft(nfail_frec)

        if falla.min()< n_falla.min():
            print("falla_max",falla.min(), "no falla max",n_falla.min())
            print("EXISTE FALLA FRECUENCIA")
        else:
            print("NO EXISTE FALLA FRECUENCIA")

        plt.plot(time[initial:final], falla[initial:final], color = 'green')
        plt.plot(time[initial:final], n_falla[initial:final], color = 'blue')
        plt.title('GRAFICA SEGUNDA TRANSFORMADA FRECUENCIA')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        plt.plot(time[initial:final], fail_frec[initial:final], color = 'blue')
        plt.plot(time[initial:final], nfail_frec[initial:final], color = 'red')
        plt.title('GRAFICA COMPARACIÓN FRECUENCIA')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        plt.scatter(time[initial:final], fail_frec[initial:final], color = 'blue')
        plt.scatter(time[initial:final], nfail_frec[initial:final], color = 'red')
        plt.title('GRAFICA VERIFICACIÓN FRECUENCIA')
        plt.xlabel('FRECUENCY')
        plt.ylabel('ESPECTRO [DB]')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()


if __name__ == "__main__": 
    app = Data_analisys(None)
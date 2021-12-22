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

        f_amplitude = pd.read_excel('falla_amplitud.xlsx', sheet_name = ['data'])
        df_famp = f_amplitude['data']
        print(df_famp)
        df_famp.plot(x = 'AMPLITUD', y = 'TIEMPO')
        plt.show()

        nfa_amplitud = [] 
        nfa_tiempo = []
        nfa_famplitud = []

        for x in range(initial, final):
            nfa_tiempo.append(df_famp.TIEMPO[x])
            nfa_amplitud.append(df_famp.NF_AMPLITUD[x])
            nfa_famplitud.append(df_famp.F_AMPLITUD[x])

        plt.plot(nfa_tiempo, nfa_amplitud, color = 'blue')
        plt.plot(nfa_tiempo, nfa_famplitud, color = 'red')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()
        plt.show()


        frecuencia = pd.read_excel('no_falla_frecuencia.xlsx', sheet_name = ['data'])
        df_nffrec = frecuencia['data']
        print(df_nffrec)
        
        nff_frecuencia = [] 
        nff_tiempo = []
        nff_ffrecuencia = []

        for x in range(initial, final):
            nff_tiempo.append(df_nffrec.TIEMPO[x])
            nff_frecuencia.append(df_nffrec.NF_FRECUENCIA[x])
            nff_ffrecuencia.append(df_nffrec.F_FRECUENCIA[x])

        plt.plot(nff_tiempo, nff_frecuencia, color = 'blue')
        plt.plot(nff_tiempo, nff_ffrecuencia, color = 'red')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()
        plt.show()
        





if __name__ == "__main__": 
    app = Data_analisys(None)
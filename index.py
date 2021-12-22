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
        # Fallas 
        f_amplitude = pd.read_excel('falla_amplitud.xlsx', sheet_name = ['data'])
        df_famp = f_amplitude['data']
        print(df_famp)
        df_famp.plot(x = 'AMPLITUD', y = 'TIEMPO')
        plt.show()

        
        fa_amplitud = []
        fa_tiempo = []
        fa_data_form = []
        fa_data_form1 = []
        fa_s = []
        # df_famp.AMPLITUD.to_numpy()
        # print(df_famp.AMPLITUD.to_numpy())

        for x in range(initial, final):
            fa_amplitud.append(df_famp.AMPLITUD[x])
            fa_tiempo.append(df_famp.TIEMPO[x])
            fa_data_form.append(df_famp.WaveformData[x])
            fa_data_form1.append(df_famp.WaveformData1[x])
            fa_s.append(np.sin(40 * 2 * np.pi * df_famp.AMPLITUD[x]) + 0.5 * np.sin(90 * 2 * np.pi * df_famp.AMPLITUD[x]))

        data = {
            'amplitud': fa_amplitud,
            'tiempo': fa_tiempo,
            'data_form': fa_data_form,
            'data_form1': fa_data_form1
        }
        df = pd.DataFrame(data)
        
        print(df)
        print('amplitud', fa_amplitud)
        print('tiempo', fa_tiempo)
        print('data', fa_data_form)
        print('data1', fa_data_form1)

        plt.plot(fa_amplitud, fa_tiempo, color = 'black')
        plt.show()
        plt.plot(fa_amplitud, fa_s, color = 'green')
        plt.show()
        
        f_frecuencia = pd.read_excel('falla_frecuencia.xlsx', sheet_name = ['data'])
        df_ffrec = f_frecuencia['data']
        print(df_ffrec)
        df_ffrec.plot(x = 'FRECUENCIA', y = 'TIEMPO')
        plt.show()

        ff_frecuencia = []
        ff_tiempo = []
        ff_data_form = []
        ff_data_form1 = []

        for x in range(initial, final):
            ff_frecuencia.append(df_ffrec.FRECUENCIA[x])
            ff_tiempo.append(df_ffrec.TIEMPO[x])
            ff_data_form.append(df_ffrec.WaveformData[x])
            ff_data_form1.append(df_ffrec.WaveformData1[x])

        plt.plot(ff_frecuencia, ff_tiempo, color = 'black')
        plt.show()
        
        # No fallas
        nf_amplitude = pd.read_excel('no_falla_tiempo.xlsx', sheet_name = ['data'])
        df_nfamp = nf_amplitude['data']
        df_nfamp.plot(x = 'AMPLITUD', y = 'TIEMPO')
        plt.show()
        nfa_amplitud = []
        nfa_tiempo = []
        nfa_data_form = []
        nfa_data_form1 = []
        nfa_s = []
        # df_famp.AMPLITUD.to_numpy()
        # print(df_famp.AMPLITUD.to_numpy())

        for x in range(initial, final):
            nfa_amplitud.append(df_nfamp.AMPLITUD[x])
            nfa_tiempo.append(df_nfamp.TIEMPO[x])
            nfa_data_form.append(df_nfamp.WaveformData[x])
            nfa_data_form1.append(df_nfamp.WaveformData1[x])
            nfa_s.append(np.sin(40 * 2 * np.pi * df_nfamp.AMPLITUD[x]) + 0.5 * np.sin(90 * 2 * np.pi * df_nfamp.AMPLITUD[x]))

        
        data = {
            'amplitud': nfa_amplitud,
            'tiempo': nfa_tiempo,
            'data_form': nfa_data_form,
            'data_form1': nfa_data_form1
        }
        df = pd.DataFrame(data)
        
        print(df)
        print('amplitud', nfa_amplitud)
        print('tiempo', nfa_tiempo)
        print('data', nfa_data_form)
        print('data1', nfa_data_form1)

        plt.plot(nfa_amplitud, nfa_tiempo, color = 'black')
        plt.show()
       
        plt.plot(nfa_amplitud, nfa_s, color = 'green')
        plt.show()


        nf_frecuencia = pd.read_excel('no_falla_frecuencia.xlsx', sheet_name = ['data'])
        df_nffrec = nf_frecuencia['data']
        print(df_nffrec)
        df_nffrec.plot(x = 'FRECUENCIA', y = 'TIEMPO')
        plt.show()

        nff_frecuencia = [] 
        nff_tiempo = []
        nff_data_form = []
        nff_data_form1 = []

        for x in range(initial, final):
            nff_frecuencia.append(df_nffrec.FRECUENCIA[x])
            nff_tiempo.append(df_nffrec.TIEMPO[x])
            nff_data_form.append(df_nffrec.WaveformData[x])
            nff_data_form1.append(df_nffrec.WaveformData1[x])

        plt.plot(nff_frecuencia, nff_tiempo, color = 'black')
        plt.show()
        

        ########################
        ## COMPARATE ###
        plt.plot(fa_amplitud, fa_tiempo, color = 'blue')
        plt.plot(nfa_amplitud, nfa_tiempo, color = 'red')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()

        plt.plot(ff_frecuencia, ff_tiempo, color = 'blue')
        plt.plot(nff_frecuencia, nff_tiempo, color = 'red')
        plt.xlabel('TIME')
        plt.ylabel('AMPLITUDE')
        plt.legend(['FAIL', 'NO FAIL'], loc='upper left')
        plt.show()


if __name__ == "__main__": 
    app = Data_analisys(None)
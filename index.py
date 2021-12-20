import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Application Class
class Data_analisys():
    #Método constructor de la clase
    def __init__(self, parent = None):
        # Fallas 
        f_amplitude = pd.read_excel('falla_amplitud.xlsx', sheet_name = ['data'])
        df_famp = f_amplitude['data']
        # print('HEAD',df_famp.head())
        leng = 80
        amplitud = []
        tiempo = []
        data_form = []
        data_form1 = []
        # df_famp.AMPLITUD.to_numpy()
        # print(df_famp.AMPLITUD.to_numpy())

        for x in range(0, leng):
            amplitud.append(df_famp.AMPLITUD[x])
            tiempo.append(df_famp.TIEMPO[x])
            data_form.append(df_famp.WaveformData[x])
            data_form1.append(df_famp.WaveformData1[x])

        data = {
            'amplitud': amplitud,
            'tiempo': tiempo,
            'data_form': data_form,
            'data_form1': data_form1
        }
        df = pd.DataFrame(data)
        
        print(df)
        print('amplitud', amplitud)
        print('tiempo', tiempo)
        print('data', data_form)
        print('data1', data_form1)

        plt.plot(amplitud, tiempo, color = 'black')
        plt.show()
        plt.plot(amplitud, data_form, color = 'blue')
        plt.show()
        plt.plot(amplitud, data_form1, color = 'red')
        plt.show()
        print(df_famp)
        
        f_frecuencia = pd.read_excel('falla_frecuencia.xlsx', sheet_name = ['data'])
        df_ffrec = f_frecuencia['data']
        print(df_ffrec)
        df_ffrec.plot(x = 'TIEMPO', y = 'FRECUENCIA')
        plt.show()

        # No fallas
        nf_amplitude = pd.read_excel('no_falla_tiempo.xlsx', sheet_name = ['data'])
        df_nfamp = nf_amplitude['data']
        print(df_nfamp)
        df_nfamp.plot(x = 'TIEMPO', y = 'AMPLITUD')
        plt.show()

        nf_frecuencia = pd.read_excel('no_falla_frecuencia.xlsx', sheet_name = ['data'])
        df_nffrec = nf_frecuencia['data']
        print(df_nffrec)
        df_nffrec.plot(x = 'TIEMPO', y = 'FRECUENCIA')
        plt.show()





if __name__ == "__main__": 
    app = Data_analisys(None)
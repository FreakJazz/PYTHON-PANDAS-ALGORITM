import sys
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

option = '0'
count =  0
period = 1

#############################################
########## BLUETOOTH ########################
#############################################

def config_bluetooth():
     
    addr = "50:3D:C6:C1:69:AB"
    service_matches = find_service( address = addr )
    buf_size = 1024;
        
    if len(service_matches) == 0:
        print("couldn't find the SampleServer service =(")
        sys.exit(0)

    for s in range(len(service_matches)):
        print("\nservice_matches: [" + str(s) + "]:")
        print(service_matches[s])
        
    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    port=2
    print("connecting to \"%s\" on %s, port %s" % (name, host, port))

    # Create the client socket
    sock=BluetoothSocket(RFCOMM)
    sock.connect((host, port))
    print("connected")
    
def graphics_with_data(initial, final):

    #########################################################
    ################### FRECUENCIA ##########################
    #########################################################

    frecuencia = pd.read_excel('no_falla_frecuencia.xlsx', sheet_name = ['data'], engine = 'openpyxl')
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
        input_and_send('a') ## la letra a representa falla en la app
        print("EXISTE FALLA BARRAS ROTAS")
    else:
        input_and_send('d') ## la letra d representa no falla en la app
        print("NO EXISTE FALLA")

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

    ###########################################################
    ############### BARRAS ROTAS ##############################
    ###########################################################
    
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

#     if barras.min() < sano.min():
#         print("EXISTE FALLA BARRAS ROTAS")
#     else:
#         print("NO EXISTE FALLA BARRAS ROTAS")

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
        

def graphics_in_real(count):
    
    df_motor_sano = pd.read_csv('motor_sano.CSV')
    fail_ms = df_motor_sano['Data1']
    fail_ms = fail_ms.to_numpy()
    fail_ms1 = []
    data_real = []
    
    for x in range(0, len(fail_ms)):
        fail_ms1.append(fail_ms[x]+25)
        data_real.append(fun_data())
        
    falla = np.fft.fft(data_real)
    sano = np.fft.fft(fail_ms1)
    
    if count >= length -1:
        count = 0
    else :
        resp = nfail_amp[count]-data1
        if resp > 0:
            input_and_send('a') ## la letra a representa falla en la app
            print('Existe falla se envio la a', resp, nfail_amp[count], data1)
        else:
            input_and_send('d') ## la letra d representa no falla en la app
            print('Existe falla se envio la a', resp, nfail_amp[count], data1)
        count +=1
    time.sleep(1)
    
    #rx_and_echo()
    
def fun_data():
        data1 = bus.read_byte_data(address, 1)
    
        return data1
    
def input_and_send(data):
    addr = "50:3D:C6:C1:69:AB"
    service_matches = find_service( address = addr )

    buf_size = 1024;

    if len(service_matches) == 0:
        print("couldn't find the SampleServer service =(")
        sys.exit(0)

    for s in range(len(service_matches)):
        print("\nservice_matches: [" + str(s) + "]:")
        print(service_matches[s])
        
    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]
    port=2
    # Create the client socket
    sock=BluetoothSocket(RFCOMM)
    sock.connect((host, port))
    print("connected")
    #while True:
        # data = input()
        #if len(data) == 0: break
    sock.send(data)
    sock.send("\n")
    sock.close()
    
def rx_and_echo():
    sock.send("\nsend anything\n")
    while True:
        data = sock.recv(buf_size)
        if data:
            print(data)
            sock.send(data)

while 1:
    
    
    if option == '0':
        
        config_bluetooth()
        print("Programa de analisis de un sistema de falla de motores.")
        print("Modo 1: Tabla de datos almacenados previamente.")
        print("Modo 2: Ingreso de datos mediante sensores")
        option = input("Ingrese el modo de trabajo: ")
        df_barras_rotas = pd.read_csv('barras_rotas.CSV')
        df_corto_circuito = pd.read_csv('cortocircuito1.CSV')
        df_motor_sano = pd.read_csv('motor_sano.CSV')
        fail_ms1 = []
        data_real = []
        fail_ms1 = []
        
    if option == '1':
        option = '1'
        initial = 0
        final = 200
        graphics_with_data(initial, final)

        break

    elif option == '2':
        
        option = '2'
        
        # i2c config
        bus = SMBus(1)
        address = 0x40
        
        graphics_in_real(count)
    

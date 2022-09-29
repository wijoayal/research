import sys
import requests
import json
import numpy 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

def myfunc(argv):
    response_API = requests.get('https://ms-data-manager.herokuapp.com/routers/', verify=False)
    data = response_API.text
    routers = json.loads(data)
    datos = []
    con = 0
    for router in routers:
        for interface in router["interfaces"]:
            con2 = 0
            if (con==0 & (con2==1 | con2==2 | con2==3 | con2==4)) | (con==1 & (con2==2 | con2==3)) | (con==2 & (con2==1 | con2==2)) | (con==3 & (con2==1 | con2==2 | con2==3)):
                dato = [float(router["rib"]["active_routes_count"]),float(router["as_number"]),float(router["rib"]["backup_routes_count"]),float(interface["bandwidth"]),float(interface["bytes_sent"]), float(interface["carrier_transitions"]),
                float(interface["crc_errors"]),float(router["rib"]["deleted_routes_count"]),float(interface["input_data_rate"]),float(interface["input_drops"]),float(interface["input_errors"]),float(interface["input_load"]),
                float(interface["input_packet_rate"]),float(interface["load_interval"]),float(router["fib"]["no_route_packets"]),float(interface["output_data_rate"]),float(interface["output_drops"]),float(interface["output_load"]),
                float(interface["output_packet_rate"]),float(interface["packets_received"]),float(router["rib"]["paths_count"]),float(router["rib"]["protocol_route_memory"]),float(interface["reliability"]),float(router["rib"]["routes_counts"])]
                datos.append(dato)
            con2+=1
        con+=1
    entrada = numpy.array(datos)
    entradaFinal =  numpy.reshape(entrada, (entrada.shape[0], 1, entrada.shape[1]))


    model2 = Sequential()
    model2.add(LSTM(24, input_shape=(entradaFinal.shape[1], entradaFinal.shape[2])))
    model2.add(Dense(3, activation="softmax")) 
    model2.compile(loss='mean_squared_error', optimizer='adam',metrics=['accuracy'])
    model2.load_weights('mnist.model.best.hdf5')
    yhat = model2.predict(entradaFinal)
    #print(yhat)
    resultado = []
    for x in yhat:
        if ((x[0]>x[1]) & (x[0]>x[2])):
            resultado.append("Normal")
        elif ((x[1]>x[0]) & (x[1]>x[2])):
            resultado.append("BGP_Clear")
        elif ((x[2]>x[1]) &  (x[2]>x[2])):
            resultado.append("Port_Flap")
        else:
            resultado.append("Normal")

    print(resultado)
    response = {
        '1.1.1.1':{

        },
        '1.1.1.2':{
            'int_g0':resultado[0],
            'int_g1':resultado[1],
            'int_g2':resultado[2],
            'int_g3':resultado[3],
        },
        '1.1.1.3':{

        },
        '1.1.1.4':{

        },
    }


if __name__ == "__main__":
    myfunc(sys.argv)
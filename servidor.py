# Descripcion:
#   El servidor se encarga de escuchar a través del socket las diversas
#   peticiones que le hagan los clientes que se coneccten a el.

import socket
import json
from coordinador import Coordinador
from crearCuentas import *

# Se crea un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verificar para logar conexión entre diferentes PC
# Se vincula el socket con el puerto
direccionServidor = ('localhost', 4444)
sock.bind(direccionServidor)

# Número máximo de conexiones que escuchará el servidor
sock.listen(5)

# Se generan la cuentas bancarias
# crearCuentas(50)

# Se inicia el coordinador de transacciones
c = Coordinador()

while True:
    conexion, direccionCliente = sock.accept()

    # Se reciben los datos
    datos = conexion.recv(4096)
    
    if datos:
        # Se formatean los datos para que sean enviados a JSON
        p = json.loads(datos)

        # Caso en el que se abre el socket, se inicia la transacción
        if(p['iniciar'] == True):
            print('iniciarTransaccion')
            r = c.iniciarTransaccion()
            print('iniciarTransaccion datos',r)
            conexion.sendall(str(r))
        elif(p['token']):
            print('hacer::')
            r = c.hacer(p['token'], p['accion'], p['param'] )
            print(r)
            conexion.sendall(str(r))
        else:
            conexion.sendall(str('ERROR'))

    else:
        print('Sin datos', direccionCliente)
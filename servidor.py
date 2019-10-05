# Descripcion:
#   El servidor se encarga de escuchar a través del socket las diversas
#   peticiones que le hagan los clientes que se conecten a el.
#
#	Cada que un cliente desee realizar alguna operación sobre la cuenta
#	se creará una nueva conexión entre este y el servidor, de tal forma
#	que la conexión que se establece no es persistente.

from operacion import Operacion
from historial import agregarHistorial
import socket
import json

# Se crea un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verificar para logar conexión entre diferentes PC
# Se vincula el socket con el puerto
direccionServidor = ('localhost', 4444)
sock.bind(direccionServidor)

# Número máximo de conexiones que escuchará el servidor
sock.listen(10)

# Se inicia el coordinador de transacciones
c = Operacion()

while True:
    conexion, direccionCliente = sock.accept()

    # Se reciben los datos
    datos = conexion.recv(4096)
    
    if datos:
        # Se formatean los datos para que sean enviados a JSON
        p = json.loads(datos)

        # Se abre el socket para inicar la transacción y se
        # devuelve el token asignado al cliente que accedio 
        # a la cuenta
        if(p['iniciar'] == True):
            agregarHistorial(' Inicia transacción ')
            r = c.abrirTransaccion()
            agregarHistorial(' Inicia transacción datos ' + r)
            conexion.sendall(str(r).encode())
        # Se ejecuta el método hacer de la instancia del coordinadorse 
        # Se envia: 
        #	- El token asignado al cliente al comenzar a operar sobre la cuenta
        #	- La operación que se desea realizar
        #	- Los parametros proporcionados por el cliente dependiendo de la
        #	  operación a realizar sobre la cuente
        # Se regresa:
        # 	- La respuesta de ejecutar la operación indicada sobre la cuenta
        elif(p['token']):
            agregarHistorial(' Hacer -> ')
            r = c.operar(p['token'], p['operacion'], p['parametros'])
            agregarHistorial(' Respuesta ' + str(r))
            conexion.sendall(str(r).encode())
        else:
            conexion.sendall(str('ERROR').encode())

    else:
    	agregarHistorial(' Sin datos **** ' + str(direccionCliente))

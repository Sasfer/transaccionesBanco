#-*- coding: utf-8-*-
# Descripcion:
#   El servidor se encarga de escuchar a traves del socket las diversas
#   peticiones que le hagan los clientes que se conecten a el.
#
#	Cada que un cliente desee realizar alguna operacion sobre la cuenta
#	se creara una nueva conexión entre este y el servidor, de tal forma
#	que la conexión que se establece no es persistente.

from operacion import Operacion, generarPassword
from historial import agregarHistorial
import socket, json, thread

# Se crea un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verificar para logar conexión entre diferentes PC
# Se vincula el socket con el puerto
direccionServidor = ('localhost', 4444)
sock.bind(direccionServidor)

print(' >> Servidor iniciado ')

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
        p = json.loads(datos.decode('utf-8'))

        # Se abre el socket para inicar la transacción y se
        # devuelve el token asignado al cliente que accedio 
        # a la cuenta
        if(p['iniciar'] == True):
            agregarHistorial(' S ** Cliente ' + p.get('cliente') +' inicia sesion ')
            r = c.abrirTransaccion()
            agregarHistorial(' S ** Inicia transaccion datos ' + r)
            conexion.sendall(str(r).encode())
        # Se ejecuta el método hacer de la instancia de operación se 
        # Se envia: 
        #	- El token asignado al cliente al comenzar a operar sobre la cuenta
        #	  mas el token que se creo para la operación en ese momento
        #	- La operación que se desea realizar
        #	- Los parametros proporcionados por el cliente dependiendo de la
        #	  operación a realizar sobre la cuente
        # Se regresa:
        # 	- La respuesta de ejecutar la operación indicada sobre la cuenta
        elif(p.get('token')):
        	# Se crea un token para la operacion
            transaccionToken = generarPassword(6)
            agregarHistorial(' S ** Hacer -> ')
            # Se ejecuta la operacion, 
            r = c.operar(p.get('token') + transaccionToken, p.get('operacion'), p.get('parametros'))
            agregarHistorial(' S ** Respuesta ' + str(r))
            conexion.sendall(str(r).encode())
        else:
            conexion.sendall(str('ERROR EN LA TRANSACCION').encode())

    else:
    	agregarHistorial(' S ** Sin datos **** ' + str(direccionCliente))

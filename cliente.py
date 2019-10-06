# Descripción:
#	El cliente se encarga de indicar que operación se aplicará 
#	sobre la cuenta, en general el procedimiento que sigue cada
#   operación es el siguiente:
#   	- Realizar conexión con el servidor
#       - Definir una solicitud (petición), compuesta por token, operación y parametros
#	- Enviar petición a través de un JSON, para que el servidor lo interprete
#       - Generar un mensaje para el agregarHistorial
#       - Generar una notificación para el cliente
#	- Cerrar conexión con el servidor

import socket, time, json, threading
from tkinter import messagebox
from historial import agregarHistorial

direccionServidor = ('localhost', 4444)

# Definición para tratar la impresión de los valores de la cuenta
def impresion(respuesta):
    respuesta = str(respuesta).replace("'","")
    return respuesta.replace("b","")

class Cliente():
    # Definición para crear un cliente
    def __init__(self,nombreCliente):
        self.nombreCliente = nombreCliente
        self.sock = None
        self.token = None
        self.solicitud = {'token':None,'operacion':None,'parametros':None}
    
    # Definición para iniciar un socket
    def iniciarSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(direccionServidor)

    # Definición para iniciar una sesión
    def iniciarSesion(self):
        self.iniciarSocket()
        self.solicitud = {'iniciar':True}
        peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(peticionJSON.encode())
        token = self.sock.recv(4096)
        if(len(token) == 10):
            self.token = token
            agregarHistorial(' C ** Inicio sesión ' + str(self.nombreCliente) + ' > T: ' + str(self.token))
            messagebox.showinfo("Bienvenido", "Ha iniciado sesión " + self.nombreCliente)
        else:
            self.token = None
            agregarHistorial(' C ** Error al iniciar sesión ' + str(self.nombreCliente) + ' > T: ' + str(self.token))
            messagebox.showinfo("Error", "No se ha podido iniciar sesión " + str(self.nombreCliente) + ". Intente de nuevo")
        self.cerrarSocket()

    # Definición para realizar una consulta
    def consultar(self):
        self.iniciarSocket()
        self.solicitud = {'token':str(self.token),'operacion':'consultar','parametros':False,'iniciar':False}
        peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(peticionJSON.encode())
        respuesta = self.sock.recv(4096)
        agregarHistorial(' C ** Consulta por > ' + str(self.nombreCliente) + ' Saldo actual: ' + str(impresion(respuesta)) + ' > T: ' + str(self.token))
        messagebox.showinfo("Consulta SALDO", str(self.nombreCliente) + " el saldo actual de la cuenta es de $ " + str(impresion(respuesta)))
        self.cerrarSocket()

    # Definición para realizar un deposito
    def depositar(self, monto):
        self.iniciarSocket()
        self.solicitud = {'token':str(self.token),'operacion':'depositar','parametros':monto,'iniciar':False}
        peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(peticionJSON.encode())
        respuesta = self.sock.recv(4096)
        agregarHistorial(' C ** Deposito por > ' + str(self.nombreCliente) + ' Saldo actual: ' + str(impresion(respuesta)) + ' > T: ' + str(self.token))
        messagebox.showinfo("Deposito", str(self.nombreCliente) + " realizo un deposito de $ " + str(monto) + ' Saldo actual $ ' + str(impresion(respuesta)))
        self.cerrarSocket()

    # Definición para realizar un retiro
    def retirar(self, monto):
        self.iniciarSocket()
        self.solicitud = {'token':str(self.token),'operacion':'retirar','parametros':monto,'iniciar':False}
        peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(peticionJSON.encode())
        respuesta = self.sock.recv(4096)
        agregarHistorial(' C ** Retiro por > ' + str(self.nombreCliente) + ' Saldo actual: ' + str(impresion(respuesta)) + ' > T: ' + str(self.token))
        messagebox.showinfo("Retiro", str(self.nombreCliente) + " realizo un retiro de $ " + str(monto) + '  Saldo actual $ ' + str(impresion(respuesta)))
        self.cerrarSocket()

    # Definición para cerrar una sesión
    def cerrarSesion(self):
        self.iniciarSocket()
        self.solicitud = {'token':str(self.token),'operacion':'cerrarSesion','parametros':None,'iniciar':False}
        peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(peticionJSON.encode())
        respuesta = self.sock.recv(4096)
        agregarHistorial(' C ** Finalizo sesión ' + str(self.nombreCliente) + ' ,' + str(impresion(respuesta)))
        messagebox.showinfo("Adios", "Ha finalizado sesión " + self.nombreCliente)
        self.sock.close()

    # Definición para cerrar un socket
    def cerrarSocket(self):
        self.sock.close()

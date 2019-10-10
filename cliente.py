#-*- coding: utf-8-*-
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
from historial import agregarHistorial, impresion

direccionServidor = ('localhost', 4444)
maxData = 4096

class Cliente():
    # Definición para crear un cliente
    def __init__(self, nombreCliente):
        self.nombreCliente = nombreCliente
        self.sock = None
        self.token = None
        self.solicitud = {'token': None, 'operacion': None, 'parametros': None}
    
    # Definición para iniciar un socket
    def iniciarSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(direccionServidor)
        except:
            agregarHistorial(' C ** Error en la conexion con el SERVIDOR')
            messagebox.showinfo("Error", "Fallo en la conexion")

    # Definición para iniciar una sesión
    def iniciarSesion(self):
        try:
            self.iniciarSocket()
            self.solicitud = {'iniciar': True, 'cliente': self.nombreCliente}
            peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
            self.sock.send(peticionJSON.encode())
            token = self.sock.recv(maxData)
            if(len(token) == 6):
                self.token = token
                agregarHistorial(' C ** Inicio sesion ' + str(self.nombreCliente) + ' > T: ' + str(impresion(self.token)))
                messagebox.showinfo("Bienvenido", "Ha iniciado sesion " + self.nombreCliente)
                self.cerrarSocket()
                # Regresa 1 si se inicio correctamente la sesión
                return 1
            else:
                self.token = None
                agregarHistorial(' C ** Error al iniciar sesion ' + str(self.nombreCliente) + ' > T: ' + str(impresion(self.token)))
                messagebox.showinfo("Error", "No se ha podido iniciar sesion " + str(self.nombreCliente) + ". Intente de nuevo")
                self.cerrarSocket()
                # Regresa 0 si no se inicio correctamente la sesión
                return 0
        except:
            agregarHistorial(" C ** No se pudo realizar la consulta")
            return 0

    # Definición para realizar una consulta
    def consultar(self):
        try:
            self.iniciarSocket()
            self.solicitud = {'token': str(self.token), 'operacion': 'consultar', 'parametros':False, 'iniciar': False}
            peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
            self.sock.send(peticionJSON.encode())
            respuesta = self.sock.recv(maxData)
            # Regresa un -1 cuando hay algun error en la transaccion
            if(respuesta == b'Se acabo el tiempo, sesion finalizada'):
                messagebox.showinfo("Notificacion","Se acabo el tiempo, sesion finalizada")
                return -1
            elif (respuesta ==b'ERROR EN LA TRANSACCION' or respuesta == b'Token invalido'):
                messagebox.showinfo("Error","Error D:")
                return -1
            else:
                agregarHistorial(' C ** Consulta por > ' + str(self.nombreCliente) + ' Saldo actual: ' + str(impresion(respuesta)))
                messagebox.showinfo("Consulta SALDO", str(self.nombreCliente) + " el saldo actual de la cuenta es de $ " + str(impresion(respuesta)))
            self.cerrarSocket()
        except:
            agregarHistorial(" C ** No se pudo realizar la consulta")
            return -1

    # Definición para realizar un deposito
    def depositar(self, monto):
        try:
            self.iniciarSocket()
            self.solicitud = {'token': str(self.token), 'operacion':'depositar', 'parametros': monto, 'iniciar': False}
            peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
            self.sock.send(peticionJSON.encode())
            respuesta = self.sock.recv(maxData)
            # Regresa un -1 cuando hay algun error en la transaccion
            if(respuesta == b'Se acabo el tiempo, sesion finalizada'):
                messagebox.showinfo("Notificacion","Se acabo el tiempo, sesion finalizada")
                return -1
            elif (respuesta ==b'ERROR EN LA TRANSACCION' or respuesta == b'Token invalido'):
                messagebox.showinfo("Error","Error D:")
                return -1
            else:
                messagebox.showinfo("Deposito", str(self.nombreCliente) + " realizo un deposito de $ " + str(monto) + '\n*** Saldo actual $ ' + str(impresion(respuesta)))
                agregarHistorial(' C ** Deposito por > ' + str(self.nombreCliente) + ' Saldo actual: ' + str(impresion(respuesta)))
            self.cerrarSocket()
        except:
            agregarHistorial(" C ** No se pudo realizar el deposito")
            return -1

    # Definición para realizar un retiro
    def retirar(self, monto):
        try:
            self.iniciarSocket()
            self.solicitud = {'token': str(self.token), 'operacion':'retirar', 'parametros':monto, 'iniciar': False}
            peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
            self.sock.send(peticionJSON.encode())
            respuesta = self.sock.recv(maxData)
            # Regresa un -1 cuando hay algun error en la transaccion
            if(respuesta == b'Se acabo el tiempo, sesion finalizada'):
                messagebox.showinfo("Notificacion","Se acabo el tiempo, sesion finalizada")
                return -1
            elif (respuesta ==b'ERROR EN LA TRANSACCION' or respuesta == b'Token invalido'):
                messagebox.showinfo("Error","Error D:")
                return -1
            # Se indica cuando no hay saldo insuficiente
            elif (respuesta == b' Saldo insuficiente'):
                messagebox.showinfo("Error","Saldo insuficiente en la cuenta" )
            # Se indica que se realizó el retiro
            else:
                messagebox.showinfo("Retiro", str(self.nombreCliente) + " realizo un retiro de $ " + str(monto) + '\n*** Saldo actual $ ' + str(impresion(respuesta)))
                agregarHistorial(' C ** Retiro por > ' + str(self.nombreCliente) + ' Saldo actual: ' + str(impresion(respuesta)))
            self.cerrarSocket()        
        except:
            agregarHistorial(" C ** No se pudo realizar el retiro")
            return -1

    # Definición para cerrar una sesión
    def cerrarSesion(self):
        try:
            self.iniciarSocket()
            self.solicitud = {'token': str(self.token), 'operacion':'cerrarSesion', 'parametros':None, 'iniciar': False}
            peticionJSON = json.dumps(self.solicitud, separators=(',', ':'))
            self.sock.send(peticionJSON.encode())
            respuesta = self.sock.recv(MAX_DATA)
            # Regresa un -1 cuando hay algun error en la transaccion
            if(respuesta == b'Se acabo el tiempo, sesion finalizada'):
                messagebox.showinfo("Notificacion","Se acabo el tiempo, sesion finalizada")
                return -1
            elif (respuesta ==b'ERROR EN LA TRANSACCION' or respuesta == b'Token invalido'):
                messagebox.showinfo("Error","Error D:")
                return -1
            else:
                agregarHistorial(' C ** Finalizo sesion ' + str(self.nombreCliente) + ' ,' + str(impresion(respuesta)))
                messagebox.showinfo("Adios", "Ha finalizado sesion " + self.nombreCliente)
            self.sock.close()
        except:
            return -1

    # Definición para cerrar un socket
    def cerrarSocket(self):
        self.sock.close()

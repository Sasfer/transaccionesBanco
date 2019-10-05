# Descripción:
#	Operación se encarga de gestionar las diferentes peticiones de ingreso a la zona critica 
#	que se presenta en la implementación de operar una cuenta bancaria.

import threading, time, socket, os, threading, signal, random, string
from datetime import timedelta
from tkinter import messagebox
from historial import agregarHistorial


# Variables globales a utilizar para operar la cuenta
timeout = None

tokenActual = None

saldo = 10000.0

bloquear = threading.Lock()
bloqueado = False


# Definición para generar una clave como identificador a los 
# hilos para gestionarlos, es decir, un token 
def generarPassword(longitud=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=longitud))


# Clase que define el tipo de transacciones que un cliente 
# tiene disponibles para aplicar a la cuenta
class Transaccion():
    # Método constructor de la clase Transacción
    def __init__(self):
        self.saldo = saldo

    # Obtiene el saldo de la cuenta
    def consultar(self):
        return self.saldo

    # Depositara un nuevo monto en la cuenta
    def depositar(self, monto):
        self.saldo = self.saldo + monto 
        return self.saldo

    # Retiro de un determinado monto de la cuenta
    def retirar(self, monto):
        self.saldo = self.saldo - monto 
        return self.saldo

# Clase que se encarga de manejar las operaciones en la cuenta 
class Operacion():
    # Método constructor de la clase Coordinador
    def __init__(self):
        global saldo
        self.saldo = saldo 

    # Se establece un tiempo de espera de 2 segundos
    def timeout(self):
        global timeout
        timeout = time.time()
        timeout += 2.0
        agregarHistorial(' Se acabo el tiempo de espera ')

    # Se revisa si la cuenta está siendo utilizado por otro cliente, 
    # en caso de ser verdadero se le notifica al cliente actual que 
    # debe esperar a que la transación externa finalice
    def abrirTransaccion(self):
        global bloqueado, tokenActual 
        agregarHistorial(' Estado cuenta >> ' + str(bloqueado))
        # Se inicia el tiempo de espera
        self.timeout()
        if(bloqueado):
            return self.abortaTransaccion(' La cuenta está siendo utilizada por otro cliente ')
        else:
            tokenActual = generarPassword()
            return self.token(tokenActual)
    
    # Implementación de las operaciones disponibles en el sistema   
    def operar(self, token, operacion, parametros=None):
        global bloqueado,tokenActual

        # Si la cuenta no está bloqueada y la solicitud es consultar 
        # el saldo,obtenemos el monto actual de la cuenta
        if(token != tokenActual and bloqueado == False and operacion == 'consultar'):
            ope = Transaccion(self.saldo)
            return ope.consultar()
    
        if(token != tokenActual):
            agregarHistorial(' >> TIEMPO DEL SERVIDOR FINALIZADO ')
            messagebox.showinfo("Notificación", "¡TIEMPO DEL SERVIDOR FINALIZADO!")
            return self.abortaTransaccion(' Token finalizado')
        
        if(timeout < time.time()):
            agregarHistorial(' >> TOKEN DEL SERVIDOR FINALIZADO **** T: ' + str(token))
            messagebox.showinfo("Notificación", "¡TOKEN DEL SERVIDOR FINALIZADO!")
            return self.abortaTransaccion(' Se acabo el tiempo, sesion finalizada')

        # Consultar no bloquea la cuenta   
        if(operacion == 'consultar'):
            agregarHistorial(' Operacion consultar ')
            ope = Transaccion(self.saldo)
            return ope.consultar()

        elif(operacion == 'depositar'):
            bloqueado = True
            agregarHistorial(' Operacion depositar ')
            ope = Transaccion(self.saldo)
            self.saldo = ope.depositar(parametros)
            return self.saldo

        elif(operacion == 'retirar'):
            bloqueado = True
            agregarHistorial(' Operacion retirar ')
            ope = Transaccion(self.saldo)
            self.saldo = ope.retirar(parametros)
            return self.saldo

        elif(operacion == 'cerrarSesion'):
            agregarHistorial(' Operacion cerrar sesión ')
            ope = Transaccion(self.saldo)
            nuevoSaldo = ope.consultar()
            if(nuevoSaldo >= 0):
                return self.cerrarTransaccion(nuevoSaldo)
            else:
                return self.abortaTransaccion(' Saldo insuficiente')

    # Se cierra la transacción
    def cerrarTransaccion(self, nuevoSaldo):
        global bloqueado,tokenActual
        agregarHistorial(' Operacion cerrar sesión ')
        saldo = nuevoSaldo
        self.saldo = saldo
        bloqueado = False
        tokenActual = None
        return saldo
    
    # Se asigna un token a la transacción
    def token(self, token):
        agregarHistorial(' Token actual ' + str(token))
        return token

    # Se aborta la transaccion si es necesario
    def abortaTransaccion(self, mensaje):
        global bloqueado,tokenActual
        agregarHistorial(' Operación aborta transaccion ')
        bloqueado = False
        tokenActual = None
        self.saldo = saldo
        return mensaje
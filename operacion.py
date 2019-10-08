# Descripción:
#	Operación se encarga de gestionar las diferentes peticiones de ingreso a la zona critica 
#	que se presenta en la implementación de operar una cuenta bancaria.

import threading, time, socket, os, threading, signal, random, string
from datetime import timedelta
from tkinter import messagebox
from historial import agregarHistorial

# Variables globales a utilizar para operar la cuenta
timeout = None

sesionFinalizada = False

tokenActual = None

saldo = 10000.0

bloqueado = False

# Definición para generar una clave como identificador a los 
# hilos para gestionarlos, es decir, un token 
def generarPassword(longitud):
	caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
	password = ""
	for i in range(longitud):
		car = random.choice(caracteres)
		password = password + car
	return password

# Clase que define el tipo de transacciones que un cliente 
# tiene disponibles para aplicar a la cuenta
class Transaccion():
    # Método constructor de la clase Transacción
    def __init__(self,saldo):
        self.saldo = float(saldo)

    # Obtiene el saldo de la cuenta
    def consultar(self):
        return self.saldo

    # Depositara un nuevo monto en la cuenta
    def depositar(self, monto):
        self.saldo = self.saldo + float(monto) 
        return self.saldo

    # Retiro de un determinado monto de la cuenta
    def retirar(self, monto):
        # Se verifica que se tenga el saldo sufiente 
        # para poder hacer un retiro
        if float(monto) > self.saldo:
            return -1
        else:
            self.saldo = self.saldo - float(monto) 
            return self.saldo

# Clase que se encarga de manejar las operaciones en la cuenta 
class Operacion():
    # Método constructor de la clase Coordinador
    def __init__(self):
        global saldo
        self.saldo = saldo 

    # Se establece un tiempo de espera para mantener la sesión abierta
    def timeout(self):
        global timeout
        timeout = time.time()
        timeout += 100.0
        agregarHistorial(' O ** Inicia el tiempo de espera ')

    # Se asigna un token a la transacción
    def token(self, token):
        agregarHistorial(' 0 ** Token actual ' + str(token))
        return token

    # Se cierra la transacción
    def cerrarTransaccion(self, nuevoSaldo):
        global bloqueado,tokenActual
        agregarHistorial(' O ** CERRAR TRANSACCIÓN')
        self.saldo = nuevoSaldo
        bloqueado = False
        tokenActual = None
        return self.saldo
    
    # Se aborta la transaccion si es necesario
    def abortaTransaccion(self, mensaje):
        global bloqueado,tokenActual
        bloqueado = False
        tokenActual = None
        return mensaje

    # Se verifica que se pueda iniciar una sesión 
    # Se revisa si la cuenta está siendo utilizado por otro cliente, 
    # en caso de ser verdadero se le notifica al cliente actual que 
    # debe esperar a que la transación externa finalice
    def abrirTransaccion(self):
        global bloqueado, tokenActual 
        agregarHistorial(' O ** Estado cuenta >> ' + str(bloqueado))
        # Se establece el tiempo que la sesión de un cliente
        # puede mantenerse abierta
        self.timeout()
        # Caso de que se este haciendo alguna transacción de 
        # retiro o depositó, no se podrá abrir una transacción,
        # es decir, no se podrá iniciar sesión
        if(bloqueado):
            agregarHistorial(' O ** ABORTA TRANSACCIÓN >> La cuenta está siendo utilizada por otro cliente ')
            return self.abortaTransaccion(' La cuenta está siendo utilizada por otro cliente ')
        else:
            tokenActual = generarPassword(10)
            return self.token(tokenActual)
    
    # Implementación de las operaciones disponibles en el sistema   
    def operar(self, token, operacion, parametros=None):
        global bloqueado,tokenActual,sesionFinalizada
    
        # Se verifica que no se haya terminado el tiempo de sesión
        if(timeout < time.time()):
            sesionFinalizada = True
            agregarHistorial(' 0 ** >> TOKEN DEL CLIENTE FINALIZADO **** T: ' + str(token))
            return self.abortaTransaccion('Se acabo el tiempo, sesion finalizada')
	        
        # Consultar no bloquea la cuenta   
        if(operacion == 'consultar'):
            agregarHistorial(' 0 ** Operacion consultar ')
            ope = Transaccion(self.saldo)
            return ope.consultar()

        elif(operacion == 'depositar'):
            bloqueado = True
            print('Entre a depositar')
            agregarHistorial(' 0 ** Operacion depositar ')
            ope = Transaccion(self.saldo)
            # Tiempo que permitira comprobar si se bloquea o no la 
            # cuenta dependiendo si se trata de lectura/escritura
            time.sleep(5)
            self.saldo = ope.depositar(parametros)
            return self.saldo

        elif(operacion == 'retirar'):
            bloqueado = True
            agregarHistorial(' 0 ** Operacion retirar ')
            ope = Transaccion(self.saldo)
            # Tiempo que permitira comprobar si se bloquea o no la 
            # cuenta dependiendo si se trata de lectura/escritura
            time.sleep(5)
            res = ope.retirar(parametros)
            # Se verifica si es posible realizar el retiro
            if (res == -1):
                agregarHistorial(' O ** ABORTA TRANSACCIÓN >> Saldo insuficiente ')
                return self.abortaTransaccion(' Saldo insuficiente')
            else:
                self.saldo = res
                return self.saldo

        elif(operacion == 'cerrarSesion'):
            agregarHistorial(' 0 ** Operacion cerrar sesión ')
            ope = Transaccion(self.saldo)
            nuevoSaldo = ope.consultar()
            return self.cerrarTransaccion(nuevoSaldo)

    
#Gestiona las diferentes peticiones de ingreso a la zona critica que en nuestra implementación
#representa una ceunta bancaria.

import threading, time, socket, os, threading, signal
from datetime import timedelta

# Variables Globales a utilizar.
tokenActual = None
saldo = 10000.0
lock = threading.Lock()
Bloqueado = False
timeout = None

#Se genera una clave como identificador a los hilos para gestionarlos. 
def generarPassword(length=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"):
    random_bytes = os.urandom(length)
    len_charset = len(charset)
    indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
    return "".join([charset[index] for index in indices])

#Definición del tipo de transacciones que estarán disponibles para realizar. 
class Transaccion():
    # Método constructor de Transacción
    def __init__(self):
        self.saldo = saldo

    # Obtiene el saldo de la cuenta
    def obtenerSaldo(self):
        return self.saldo

    # Depositara un nuevo saldo en la cuenta
    def depositar(self, monto):
        self.saldo += monto 
        return self.saldo

    # Retiro de un determinado monto a la cuenta
    def retirar(self, monto):
        self.saldo -= monto 
        return self.saldo

#Clase Coordinadora se encarga de manejar las operaciones en la cuenta 
class Coordinador():
    # Método constructor de la clase Coordinador
    def __init__(self):
        global saldo
        self.saldo = saldo # global

    # Se registra la hora en la cual una transación fue terminada
    def timeout(self):
        global timeout
        timeout = time.time()
        timeout += 2.0
        print('TODO: TIMEOUT ')

    #Se revisa si el recurso está siendo utilizado por otro usuario, en caso de ser verdadero se le notifica al cliente que debe esperar a que la transación externa finalice. 
    def abrirTrans(self):
        global Bloqueado,tokenActual
        print('Bloqueado',Bloqueado)
        self.timeout() # INIT TIMEOUT
        if(Bloqueado):
            return self.abortaTrans('El recurso está siendo utilizado por otro usuario')
        else:
            tokenActual = generarPassword()
            #Bloqueado = True
            return self.token(tokenActual)
    
    # Implementación de las operaciones disponibles en el sistema.   
    def hacer(self, token, movimiento, param=None):
        # Si el estado no está bloqueado y la solicitud es obtener el saldo, obtenemos el monto actual de la cuenta.
        global Bloqueado,tokenActual
        if(token != tokenActual and Bloqueado == False and movimiento == 'obtener_saldo'):
            t = Transaccion(self.saldo)
            return t.obtener_saldo()
        
        if(token != tokenActual):
            print(':: TIEMPO DEL SERVIDOR EXPIRADO ::' )
            return self.abortaTransaccion('Token expirado')
        
        if(timeout < time.time() ):
            print(':: TOKEN DEL SERVIDOR EXPIRADO ::' , token )
            return self.abortaTransaccion('Se acabo el tiempo, sesion expirada')

        if(movimiento == 'obtener_saldo'):
            print('coord::saldo')
            t = Transaccion(self.saldo)
            return t.obtener_saldo()

        elif(movimiento == 'depositar'):
            Bloqueado = True
            print('coord::depositar')
            Bloqueado = True
            t = Transaccion(self.saldo)
            self.saldo = t.depositar(param)
            return self.saldo

        elif(movimiento == 'retirar'):
            Bloqueado = True
            print('coord::retirar')
            t = Transaccion(self.saldo)
            Bloqueado = True
            self.saldo = t.retirar(param)
            return self.saldo

        elif(movimiento == 'cerrarSesion'):
            print('coord::cerrarSesion')
            t = Transaccion(self.saldo)
            nuevoSaldo = t.obtener_saldo()
            if(nuevoSaldo >= 0):
                return self.cerrarTransaccion(nuevoSaldo)
            else:
                return self.abortaTransaccion('Saldo insuficiente')

    # Se cierra la transferencia
    def cerrarTransaccion(self, nuevoSaldo):
        global Bloqueado,tokenActual
        print('coord::close_session')
        saldo = nuevoSaldo
        self.saldo = saldo
        Bloqueado = False
        tokenActual = None
        #print('saldo',saldo)
        return saldo
    
    # Se asigna un token a la transacción
    def token(self, token):
        print('curr', token)
        return token

    # Aborta la transaccion si es necesario
    def abortaTransaccion(self, mensaje):
        global Bloqueado,tokenActual
        print('coord::abortaTrans')
        Bloqueado = False
        tokenActual = None
        self.saldo = saldo # RESET saldo
        return mensaje
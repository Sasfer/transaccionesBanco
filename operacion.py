#-*- coding: utf-8-*-
# Descripción:
#	Operación se encarga de gestionar las diferentes peticiones de ingreso a la zona critica 
#	que se presenta en la implementación de operar una cuenta bancaria.

import time, socket, os, thread, signal, random, string
from Queue import Queue 
from datetime import timedelta
from tkinter import messagebox
from historial import agregarHistorial, impresion


# Cola para guardar el resultado de alguna transaccion
resultado = Queue()

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
    def consultar(self, token):
        agregarHistorial(' O ** Operacion consultar  T >> ' + str(impresion(token)))
        return self.saldo

    # Depositara un nuevo monto en la cuenta
    def depositar(self, monto, token, bloqueo):
        agregarHistorial(' O ** Operacion depositar T >> ' + str(impresion(token)))
        self.saldo = self.saldo + float(monto) 
        resultado.put(self.saldo)

    # Retiro de un determinado monto de la cuenta
    def retirar(self, monto, token, bloqueo):
        agregarHistorial(' 0 ** Operacion retirar T >> ' + str(impresion(token)))
        # Se verifica que se tenga el saldo sufiente para poder hacer un retiro
        if float(monto) > self.saldo:
            resultado.put(-1)
        else:
            self.saldo = self.saldo - float(monto) 
            resultado.put(self.saldo)

# Clase que se encarga de manejar las operaciones en la cuenta 
class Operacion():
    # Método constructor de la clase Coordinador, 
    # utiliza estas configuraciones para inicializar
    def __init__(self):
        self.aux = True
        self.timeoutVal = None
        self.sesionFinalizada = False
        self.tokenActual = None
        # Saldo inicial de la cuenta
        self.saldo = 10000.0
        # Para saber que no ha habido ningun problema al 
        # realizar alguna de las transacciones en la cuenta
        self.verificador = True
        # Para saber si la cuenta esta bloqueada o no
        self.bloqueado = False

    # Se establece un tiempo de espera para mantener la sesión abierta
    def timeout(self):
        self.timeoutVal = time.time()
        agregarHistorial(' O ** Inicia el tiempo de espera ')
        # Se establecen 2 minutos para la sesion
        self.timeoutVal += 120.0

    # Se asigna un token a la transaccion
    def token(self, token):
        agregarHistorial(' 0 ** Token actual ' + str(impresion(token)))
        return token

    # Se verifica que se pueda iniciar una sesión 
    # Se revisa si la cuenta está siendo utilizado por otro cliente, 
    # en caso de ser verdadero se le notifica al cliente actual que 
    # debe esperar a que la transación externa finalice
    def abrirTransaccion(self):
        agregarHistorial(' O ** Estado cuenta >> ' + str(self.bloqueado))
        # Se establece el tiempo que la sesión de un cliente
        # puede mantenerse abierta
        self.timeout()
        # Caso de que se este haciendo alguna transacción de 
        # retiro o depositó, no se podrá abrir una transaccion,
        # es decir, no se podrá iniciar sesion
        if(self.bloqueado):
            agregarHistorial(' O ** ABORTA TRANSACCIÓN >> La cuenta esta siendo utilizada por otro cliente ')
            return self.abortaTransaccion(' La cuenta esta siendo utilizada por otro cliente ')
        else:
            self.tokenActual = generarPassword(6)
            return self.token(self.tokenActual)

    # Se cierra la transaccion
    def cerrarTransaccion(self, nuevoSaldo):
        agregarHistorial(' O ** CERRAR TRANSACCION')
        self.saldo = nuevoSaldo
        self.bloqueado = False
        self.tokenActual = None
        return self.saldo
    
    # Se aborta la transaccion si es necesario
    def abortaTransaccion(self, mensaje):
        agregarHistorial(' O ** ABORTAR TRANSACCION')
        self.bloqueado = False
        self.tokenActual = None
        return mensaje
    
    # Implementación de las operaciones disponibles en el sistema   
    def operar(self, token, operacion, parametros=None):
        # Se verifica que la transaccion a implementar tenga un token
        if(str(impresion(token)) == "" or len(str(impresion(token))) != 12):
            agregarHistorial(' 0 ** >> TOKEN INVALIDO **** T: ' + str(impresion(token)))
            return self.abortaTransaccion('Token invalido')

        # Se verifica que no se haya terminado el tiempo de sesión
        if(self.timeoutVal < time.time()):
            self.sesionFinalizada = True
            agregarHistorial(' 0 ** >> TOKEN DEL CLIENTE FINALIZADO **** T: ' + str(impresion(token)))
            return self.abortaTransaccion('Se acabo el tiempo, sesion finalizada')

        # Se verifica si la cuenta esta siendo ocupada
        # En caso se que si, la transaccion se queda esperando
        while(self.bloqueado == True):
            if (self.aux == True):
                # Se registra una espera para poder modificar el recurso
                agregarHistorial(' 0 ** >> CUENTA BLOQUEDA ... ESPERANDO')
                self.aux = False
	        
        # Operacion consultar   
        if(operacion == 'consultar'):
            # La operacion consultar no requiere bloqueo
            ope = Transaccion(self.saldo)
            self.saldo = ope.consultar(token)
            return self.saldo

        elif(operacion == 'depositar'):
            self.bloqueado = True
            # Para solicitar un bloqueo si la cuenta se esta usando
            bloquear = thread.allocate_lock()
            agregarHistorial(' O ** Se bloquea la cuenta')
            # Bloqueamos la cuenta
            bloquear.acquire()
            ope = Transaccion(self.saldo)
            # Lanzamos un hilo, con la operacion, sus parametros y el bloqueo
            agregarHistorial(' O ** Se lanza un hilo')
            thread.start_new_thread(ope.depositar,(parametros,token, bloquear))
            self.saldo = resultado.get()
            # Tiempo de espera para asegurar que entre el hilo
            time.sleep(3)
            # Liberamos el bloqueo
            agregarHistorial(' O ** Se libera el bloqueo')
            bloquear.release()
            # Se espera a que termine el hilo, para hacer la liberacion del bloqueo
            agregarHistorial(' O ** Espera a termino del hilo y liberacion del bloqueo')
            bloquear.acquire()
            bloquear.release()
            self.bloqueado = False
            return self.saldo

        elif(operacion == 'retirar'):
            self.bloqueado = True
            self.verificador = True
            # Para solicitar un bloqueo si la cuenta se esta usando
            bloquear = thread.allocate_lock()
            agregarHistorial(' O ** Se bloquea la cuenta')
            # Bloqueamos la cuenta
            bloquear.acquire()
            ope = Transaccion(self.saldo)
            # Lanzamos un hilo, con la operacion, sus parametros y el bloqueo
            agregarHistorial(' O ** Se lanza un hilo')
            thread.start_new_thread(ope.retirar,(parametros,token, bloquear))
            # Tiempo de espera para asegurar que entre el hilo
            time.sleep(3)
            ret = resultado.get()
            # Se verifica si es posible realizar el retiro
            if (ret == -1):
                agregarHistorial(' O ** ABORTA TRANSACCION >> Saldo insuficiente ')
                self.bloqueado = False
                self.verificador = False
                # Liberamos el bloqueo
                agregarHistorial(' O ** Se libera el bloqueo principal')
                bloquear.release()
                # Se espera a que termine el hilo, para hacer la liberacion del bloqueo
                agregarHistorial(' O ** Espera a termino del hilo y liberacion del bloqueo')
                bloquear.acquire()
                bloquear.release()
                return self.abortaTransaccion(' Saldo insuficiente')
            else:
                self.bloqueado = False
                self.saldo = ret
                # Liberamos el bloqueo
                agregarHistorial(' O ** Se libera el bloqueo principal')
                bloquear.release()
                # Se espera a que termine el hilo, para hacer la liberacion del bloqueo
                agregarHistorial(' O ** Espera a termino del hilo y liberacion del bloqueo')
                bloquear.acquire()
                bloquear.release()
                return self.saldo

        elif(operacion == 'cerrarSesion'):
            agregarHistorial(' 0 ** Operacion cerrar sesion T >> ' + str(impresion(token)))
            ope = Transaccion(self.saldo)
            nuevoSaldo = ope.consultar(token)
            return self.cerrarTransaccion(nuevoSaldo)

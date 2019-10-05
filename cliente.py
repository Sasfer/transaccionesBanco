import socket, time, json, threading

bloquear = threading.Lock()

direccionsServidor = ('localhost', 4444)


class cliente():
    def __init__(self,nombreCliente):
        self.nombreCliente = nombreCliente
        self.sock = None
        self.token = None
        self.solicitud = { 'token': None, 'accion': None, 'param':None }
        
    def iniciarSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(direccionsServidor)

    def cerrarSocket(self):
        self.sock.close()

    def iniciarSession(self):
        self.iniciarSocket()
        self.solicitud = {'iniciar':True}
        jsonCadena = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(jsonCadena)
        token = self.sock.recv(4096)
        if(len(token) == 8):
            self.token = token
            print('iniciarSession',self.token,self.nombreCliente)
        else:
            self.token = None
            print('Error',token,self.nombreCliente)
                
        self.cerrarSocket()

    def cerrarSession(self):
        self.abrirSocket()
        self.solicitud = {'token':self.token, 'accion':'cerrarSession', 'param':None, 'abrir':False}
        jsonCadena = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(jsonCadena)
        respuesta = self.sock.recv(4096)
        self.close_sock()
        print('cerrarSession', respuesta, self.nombreCliente)

    def consultar(self):
        self.abrirSocket()
        self.solicitud = {'token':self.token, 'accion':'consultar', 'param':None,'abrir':False}
        jsonCadena = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(jsonCadena)
        respuesta = self.sock.recv(4096)
        print('consultar: ',self.nombreCliente, respuesta,self.token)
        self.cerrarSocket()

    def depositar(self, monto):
        self.cerrarSocket()
        self.solicitud = {'token':self.token, 'accion':'depositar', 'param':monto,'abrir':False}
        jsonCadena = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(jsonCadena)
        respuesta = self.sock.recv(4096)
        print('depositar: ',self.nombreCliente, respuesta,self.token)
        self.cerrarSocket()

    def retirar(self, monto):
        self.abrirSocket()
        self.solicitud = {'token':self.token, 'accion':'asignarMonto', 'param':monto, 'abrir':False}
        jsonCadena = json.dumps(self.solicitud, separators=(',', ':'))
        self.sock.send(jsonCadena)
        respuesta = self.sock.recv(4096)
        print('asignarMonto: ',self.nombreCliente,respuesta,self.token)
        self.cerrarSocket()

#x = Client('Bob')
a = Client('Alice')
#x.open_session()
a.open_session()
a.withdraw(100)
a.get_balance()

time.sleep(3)
a.close_session()

x = Client('Bob')
x.open_session()
x.get_balance()

# a.get_balance()

# #a.close_session()
# #x.close_session()
# #a.withdraw(10)
# a.get_balance()
# a.close_session()
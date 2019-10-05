# Descripción:
#	Se especifica el número de cuentas bancarias a generar
#   y se crea un archivo con los respectivos datos.
#
#	Datos de una cuenta bancaria
#		- Numero de cuenta
#       - NIP
#		- Saldo

from random import *

# Por practicidad todas las cuentas tendran el mismo NIP
nip = 1234

def crearCuentas(numCuentas):
	
	cuentasBancarias = open('cuentasBancarias.txt', 'w+')
	
	for i in range(1, numCuentas + 1):
		cuentasBancarias.write(str(i) + ',' + str(nip) + ',' + str(randrange(0, 500100, 100)) + '\n')
	
	cuentasBancarias.close()
# Descripción:
#	Dado un mensaje, se crear un archivo llamado historial en caso de que no se
#   haya creado, y se agrega el respectivo mensaje al archivo para tener un 
#	histórico de lo que se va realizando en la cuenta bancaria.

import time

def agregarHistorial(mensaje):
	
	historial = open('historial.txt', 'a+')
	
	historial.write(' >> ' + str(time.strftime("%d/%m/%y %H:%M:%S - ")) + mensaje + '\n')
	
	historial.close()
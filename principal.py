# Descripción:
#   Ventana principal del banco

from tkinter import *
from tkinter import messagebox
from crearCuentas import *
from cliente import *
from functools import partial

def ingresar():
	aux = 0

	nc = str(numCuenta.get())
	n = str(nip.get())

	if nc == "":
		messagebox.showinfo("Error", "Ingresa un número de cuenta")
	elif n == "":
		messagebox.showinfo("Error", "Ingresa tu NIP")
	else:
		cuentas = open('cuentasBancarias.txt')
		for c in cuentas.readlines():
			c.replace('\n','')
			if c.split(',')[0] == nc and c.split(',')[1] == n:
				messagebox.showinfo("Notificación", "Has ingresado")
				aux = 1
				cuentas.close()
				break

		if aux == 0:
			messagebox.showinfo("Notificación", "Numero de cuenta/NIP incorrectos")

def consultar():
	messagebox.showinfo("Información", "Consultar")

def retirar():
	messagebox.showinfo("Información", "Retirar")

def depositar():
	messagebox.showinfo("Información", "Despositar")

def salir():
	messagebox.showinfo("Información", "Salir")

# Se generan la cuentas bancarias
crearCuentas(50)

# Se crea la ventana principal
banco = Tk()
banco.title('Banco FIMSS')
banco.geometry('370x220')

numCuenta = IntVar()
nip = IntVar()
monto = IntVar()

numCuentaL = Label(banco, text="Numero de cuenta", anchor='e')
nipL = Label(banco, text="NIP", anchor='e')
montoL = Label(banco, text="Monto", anchor='e') 

numCuentaE = Entry(banco, textvariable=numCuenta, width=20, bg='white', state='normal')
nipE = Entry(banco, textvariable=nip, width=20, bg='white', state='normal')
montoE = Entry(banco, textvariable=monto, width=20, bg='white', state='disabled') 

ingresarB = Button(banco, text="Ingresar", command=ingresar, state='normal') 
consultarB = Button(banco, text="Consultar", command=consultar, state='disabled')
retirarB = Button(banco, text="Retirar", command=retirar, state='disabled')
depositarB = Button(banco, text="Depositar", command=depositar, state='disabled')
salirB = Button(banco, text="Salir", command=salir, state='disabled')

numCuentaL.place(x=20, y=20, width=120, height=25)
numCuentaE.place(x=150, y=20, width=90, height=25)
ingresarB.place(x=250, y=20, width=90, height=25)

nipL.place(x=20, y=50, width=120, height=25)
nipE.place(x=150, y=50, width=90, height=25)

montoL.place(x=20, y=100, width=120, height=25)
montoE.place(x=150, y=100, width=90, height=25)

consultarB.place(x=80, y=140, width=70, height=25)
retirarB.place(x=160, y=140, width=70, height=25)
depositarB.place(x=240, y=140, width=70, height=25)

salirB.place(x=260, y=180, width=70, height=25)

numCuentaE.delete(0,END)
nipE.delete(0,END)
montoE.delete(0,END)

banco.mainloop()

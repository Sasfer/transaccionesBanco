#-*- coding: utf-8-*-
# Descripción:
#   Ventana principal para que varios clientas puedan accesar a una misma 
#	cuenta y poder hacer diversas operaciones sobre esta.

from tkinter import *
from tkinter import messagebox
from cliente import *

cliente = None # Esto debería estar dentro de una clase para no usar variables globales

# Operación para inicar la conexión de un cliente a la cuenta
def ingresar():
	global cliente
	
	# Variables con valores capturados de la GUI del cliente
	nc = str(nombreCliente.get())
	n = str(nip.get()) 

	if nc == "" or n == "":
		messagebox.showinfo("Error", "No has ingresado el nombre del cliente o el NIP")
	else:
		messagebox.showinfo("Notificacion", "Has solicitado ingresar a la cuenta")
		
		# Creación del objeto identificador del cliente
		cliente = Cliente(nc)
		
		# Se inicia un sesión para el cliente 
		res = cliente.iniciarSesion()

		# Si la sesión se ha iniciado correctamente,
		# se habilitan los respectivos capos de transacciones
		if res == 1:
			# Se dehabilitan algunas opción de la ventana
			ingresarB.config(state='disabled')
			nombreClienteE.config(state='disabled')
			nipE.config(state='disabled')

			# Se habilitam algunas opciones de la ventana
			montoE.config(state='normal')
			consultarB.config(state='normal')
			depositarB.config(state='normal')
			retirarB.config(state='normal')
			salirB.config(state='normal')

			# Se limpia el campo de monto
			montoE.delete(0,END)
			
# Operación para hacer una consulta del estado de la cuenta
def consultar():
	global cliente
	messagebox.showinfo("Notificacion", "Has solicitado consultar la cuenta")

	# Se realiza una consulta a la cuenta
	res = cliente.consultar()

	# Si la sesión finalizo, se regresa a iniciar sesión de nuevo
	if(res == -1):
		cliente.cerrarSesion()

		# Se dehabilitan algunas opción de la ventana
		ingresarB.config(state='normal')
		nombreClienteE.config(state='normal')
		nipE.config(state='normal')

		# Se habilitam algunas opciones de la ventana
		montoE.config(state='disabled')
		consultarB.config(state='disabled')
		depositarB.config(state='disabled')
		retirarB.config(state='disabled')
		salirB.config(state='disabled')

		# Limpia los campo de nombre y NIP
		nombreClienteE.delete(0,END)
		nipE.delete(0,END)
	
	# Se limpia el campo de monto
	montoE.delete(0,END)

# Operación de retiro de la cuenta
def retirar():
	global cliente

	# Variable con el valor capturado de la GUI del cliente
	m = str(montoE.get())

	if m == "":
		messagebox.showinfo("Notificacion", "No has ingresado el monto a retirar")	
	else:
		messagebox.showinfo("Notificacion", "Has solicitado hacer un retiro de la cuenta")	
		
		# Se realiza un retiro a la cuenta
		res = cliente.retirar(m)

		# Si la sesión finalizo, se regresa a iniciar sesión de nuevo
		if(res == -1):
			cliente.cerrarSesion()

			# Se dehabilitan algunas opción de la ventana
			ingresarB.config(state='normal')
			nombreClienteE.config(state='normal')
			nipE.config(state='normal')

			# Se habilitam algunas opciones de la ventana
			montoE.config(state='disabled')
			consultarB.config(state='disabled')
			depositarB.config(state='disabled')
			retirarB.config(state='disabled')
			salirB.config(state='disabled')

			# Limpia los campo de nombre y NIP
			nombreClienteE.delete(0,END)
			nipE.delete(0,END)
	
	# Se limpia el campo de monto
	montoE.delete(0,END)

# Operación de depósito a la cuenta
def depositar():
	global cliente

	# Variable con el valor capturado de la GUI del cliente
	m = str(montoE.get())

	if m == "":
		messagebox.showinfo("Notificacion", "No has ingresado el monto a depositar")	
	else:
		messagebox.showinfo("Notificacion", "Has solicitado hacer un deposito a la cuenta")

		# Se realiza un deposito a la cuenta
		res = cliente.depositar(m)

		# Si la sesión finalizo, se regresa a iniciar sesión de nuevo
		if(res == -1):
			cliente.cerrarSesion()

			# Se dehabilitan algunas opción de la ventana
			ingresarB.config(state='normal')
			nombreClienteE.config(state='normal')
			nipE.config(state='normal')

			# Se habilitam algunas opciones de la ventana
			montoE.config(state='disabled')
			consultarB.config(state='disabled')
			depositarB.config(state='disabled')
			retirarB.config(state='disabled')
			salirB.config(state='disabled')

			# Limpia los campo de nombre y NIP
			nombreClienteE.delete(0,END)
			nipE.delete(0,END)
			
	# Se limpia el campo de monto
	montoE.delete(0,END)

# Operación para finalizar la aplicación
def salir():
	global cliente

	messagebox.showinfo("Notificacion", "Has solicitado salir de la cuenta")

	# Se cierra la sesión del cliente
	cliente.cerrarSesion()

	# Se dehabilitan algunas opción de la ventana
	ingresarB.config(state='normal')
	nombreClienteE.config(state='normal')
	nipE.config(state='normal')

	# Se habilitam algunas opciones de la ventana
	montoE.config(state='disabled')
	consultarB.config(state='disabled')
	depositarB.config(state='disabled')
	retirarB.config(state='disabled')
	salirB.config(state='disabled')

	# Limpia los campo de nombre y NIP
	nombreClienteE.delete(0,END)
	nipE.delete(0,END)

# Se crea la ventana principal
banco = Tk()
banco.title('Banco FIMSS')
banco.geometry('370x220')

# Obtenemos las variables de entrada de los campos input
nombreCliente = StringVar()
nip = IntVar()
monto = IntVar()

# Etiquetas para indicar el nombre de los campos input
nombreClienteL = Label(banco, text="Nombre cliente", anchor='e')
nipL = Label(banco, text="NIP", anchor='e')
montoL = Label(banco, text="Monto", anchor='e') 

# Campos de entrada a los valores seelccionados por el usuario
nombreClienteE = Entry(banco, textvariable=nombreCliente, width=20, bg='white', state='normal')
nipE = Entry(banco, textvariable=nip, width=20, bg='white', state='normal')
montoE = Entry(banco, textvariable=monto, width=20, bg='white', state='disabled') 

# Botones de interacción con la interfaz del cliente
ingresarB = Button(banco, text="Ingresar", command=ingresar, state='normal') 
consultarB = Button(banco, text="Consultar", command=consultar, state='disabled')
retirarB = Button(banco, text="Retirar", command=retirar, state='disabled')
depositarB = Button(banco, text="Depositar", command=depositar, state='disabled')
salirB = Button(banco, text="Salir", command=salir, state='disabled')

# Se ubica espacialmente en el GUI la etiqueta y campo cliente, así como el botón ingresar
nombreClienteL.place(x=20, y=20, width=120, height=25)
nombreClienteE.place(x=150, y=20, width=90, height=25)
ingresarB.place(x=250, y=20, width=90, height=25)

# Se ubica espacialmente en el GUI la etiqueta y campo nip
nipL.place(x=20, y=50, width=120, height=25)
nipE.place(x=150, y=50, width=90, height=25)

# Se ubica espacialmente en el GUI la etiqueta y campo de monto
montoL.place(x=20, y=100, width=120, height=25)
montoE.place(x=150, y=100, width=90, height=25)

# Se ubica espacialmente en la GUI los botones de las 3 operaciones sobre la cuenta.
consultarB.place(x=80, y=140, width=70, height=25)
retirarB.place(x=160, y=140, width=70, height=25)
depositarB.place(x=240, y=140, width=70, height=25)

# Se posiciona el botón para salir de la aplicación
salirB.place(x=260, y=180, width=70, height=25)

# Se elimina el cero que es el valor inicial de los campos.
nombreClienteE.delete(0,END)
nipE.delete(0,END)

# Loop para mantener renderizada la ventana de tkinter
banco.mainloop()

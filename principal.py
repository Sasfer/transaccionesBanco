# Descripción:
#   Ventana principal para que varios clientas puedan accesar a una misma 
#	cuenta y poder hacer diversas transacciones

from tkinter import *
from tkinter import messagebox
from cliente import *

# Operación para inicar la conexión de un cliente a la cuenta
def ingresar():
	validacionIngreso = 0

	# Variables con valores capturados de la GUI del cliente
	nc = str(nombreCliente.get())
	n = str(nip.get()) 
	
	# Creación del objeto identificador del cliente
	cliente = cliente(nc)
	messagebox.showinfo("Notificación", "Numero de cuenta/NIP incorrectos")

# Operación para hacer una consulta del estado de la cuenta
def consultar():
	messagebox.showinfo("Notificación", "Consultar")

# Operación de retiro de la cuenta
def retirar():
	messagebox.showinfo("Notificación", "Retirar")

# Operación de depósito a la cuenta
def depositar():
	messagebox.showinfo("Notificación", "Despositar")

# Operación para finalizar la aplicación
def salir():
	messagebox.showinfo("Notificación", "Salir")


# Se crea la ventana principal
banco = Tk()
banco.title('Banco FIMSS')
banco.geometry('370x220')

# Obtenemos las variables de entrada de los campos input
nombreCliente = IntVar()
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
montoE.delete(0,END)

# Loop para mantener renderizada la ventana de tkinter
banco.mainloop()

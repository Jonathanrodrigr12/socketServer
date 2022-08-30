# Importarciones para e uso de las librerias que van a crear el socket
import socket
import threading

# Input necesarios para el flujo del chat
host = '127.0.0.1'
port = 8586
username = input("Enter your username: ")

# Creación de socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Medoto connect_socket el es encargado de realizar la conexión con el socket
def connect_socket():
    try:
        client.connect((host, port))
    except:
        #esta expeción controla si no pudo obtener conexión finaliza el programa
        print("No se pudo conectar")
        exit()

connect_socket()

# Medoto receive_messages el cúal se encarga de recbir mensajes
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))  
            else:
                message_identifier = message
                print(f"{message_identifier}\n")
        except:
            # esta expeción finaliza el cliclo cuando causa alguna expeción con el socket
            break

# Medoto write_messages el cúal se encarga de escribir los mensajes
def write_messages():
    while True:
        try:
            print("1. Insertar \n") 
            print("2. Consultar \n") 
            operation = input("")
            account = ''
            balance = ''
            if operation == "1":
                account = input("Cuenta a insertar\n")
                balance = input("Saldo a insertar\n")
            elif operation == "2":
                account = input("Cuenta a consultar\n")
            message = f"{operation}:{account},{balance}"
            client.send(message.encode('utf-8'))
        except:
             # esta expeción finaliza el cliclo cuando causa alguna expeción con el socket
            break    

# creacion de hilo indepeniente para recibir mensajes
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# creacion de hilo indepeniente para escribir mensajes
write_thread = threading.Thread(target=write_messages)
write_thread.start()
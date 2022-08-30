# Importarciones para e uso de las librerias que van a crear el socket

import socket   
import threading


# Host y puerto por el cúal va hacer expuesto el socket
host = '127.0.0.1'
port = 8586


# Creación de socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuración de como se va a exponer el socket
server.bind((host, port))

# Inicialización para que el socket puede recibir conexiones
server.listen()

# Mensaje informativo de inicio del socket
print(f"Server running on {host}:{port}")


# Clients y usernames registrados en el servidor
clients = []
usernames = []

# Medoto broadcast el es encargado de enviar los mensajes a los diferentes clientes
# message: parametro que recibe el mensaje
# _cliente: cliente el cúal envio el mensaje
def broadcast(message, _client):
    for client in clients:
        if client == _client:
            client.send(message.encode("utf-8"))

# Medoto handle_messages el cúal da el manejo de los mensajes
# client: cliente que envio el mensaje
def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            mesagge_uncode = message.decode('utf-8')
            operation = mesagge_uncode.split(":")
            if operation[0] == '1':
               message = insert_file(operation[1].split(","))
            elif operation[0] == '2':
               message = get_balance(operation[1].split(","))
            broadcast(message, client)
        except:
            # esta expeción se realiza cuando falla el insert de los datos
            broadcast("No se pudo insertar/consultar la informacion", client)
            break

# Medoto insert_file el cúal inserta los registros al txt
# value: valor a insertar
def insert_file(value):
    try:
        with open('/home/jonathan.rodriguez/Documentos/muestras-hudi/data.txt', 'a') as f:
            f.write(f'{int(value[0])},{int(value[1])}\n')
        return 'Se inserto el registro correctamente'
    except:
        return 'No se pudo insertar el registro'

# Medoto get_balance el cúal obtiene el saldo respectoa  la cuenta
# value: valor a consultar
def get_balance(value):
    with open('/home/jonathan.rodriguez/Documentos/muestras-hudi/data.txt') as f:
        data = f.readlines()
        result = [x for x in data if x.split(",")[0] == value[0]]
        return f'su saldo para la cuenta {result[0].split(",")[0]} es de {result[0].split(",")[1]}'\
            if len(result)>0 else 'No existe la cuenta'

# Medoto receive_connections el cúal se encarga de recibi las conexión y asignarle a cada cliente un handle_message independiente
def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")
        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()


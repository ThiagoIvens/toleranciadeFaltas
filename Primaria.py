import socket, threading

HOST = '127.0.0.1'       # Endereco IP do Servidor
PORT = 1001    # Porta que o Servidor esta
DEST = (HOST, PORT)
saldo = 0

def main():
    t = threading.Thread(target = recv) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

def recv():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp.bind((HOST, PORT))
    tcp.listen(5)
    request = tcp.accept()

    try:
        while True:
            print('Concetado por', request)
            data = request.recv(1024) 
            if not data: break
            print(data)
            data.decode('utf-8').split('|')
            id = data[0]
            operation = data[1]
            valor = data[2]

            print (id, operation, valor)

    finally:
        request.close()
        print('Finalizando conexao do cliente', request)

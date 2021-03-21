import socket, threading
HOST = '127.0.0.1'       # Endereco IP do Servidor
PORT = 1040    # Porta que o Servidor esta
saldo = 0
listReplicas = [1020, 1030, 1050]
contador_confirmados = 0
listValues = []

def main():
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    print("Iniciando Thread")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicia uma conexao tcp
    s.bind((HOST, PORT)) # define o destino da conexao
    s.listen() # começa a escutar no destino definido
    while True:
        con, port = s.accept() # define a conexao e atribui a variavel conn, quando o servidor aceitar
        try:
            while True:
                msg = con.recv(1024)
                if not msg: break
                data = msg.decode().split('|')
                id = data[0] # atribui o primeiro valor a variavel id
                operation1 = data[1] # atribui o segundo valor a variavel operation
                operation2 = data[2]
                valor = data[3] # atribui o terceiro valor a variavel valor
                
                print(data)

                if (operation1 == "COMPARE"):
                    # faz o codigo de OK
                    codeDentrodoIF(msg, valor, operation2)
                    
                    if contador_confirmados == 5 or len(listValues) == 5:
                        if comparar:
                            print('Todas replicas retornaram OK')
                            msg = str(id)+'|OK|'+str(saldo)
                            enviaMsg(PORT, msg)
                            contador_confirmados = 0
                    
                    elif len(listValues) != 5 and contador_confirmados !=5:
                        for replica in listReplicas:
                            enviaMsg(replica, msg)
                    
        finally:
            print('fechou conexao')
            s.close() # fexa a conexao com o servidor
            break

def comparar():
    for i in len(listValues):
        if(listValues[0] != listValues[i]):
            return False
    return True

def enviaMsg(port, data):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.connect((HOST, port))
    conexao.sendall(data.encode('utf-8'))

def codeDentrodoIF(msg, valor, operation):
    contador_confirmados +=1
    if operation == "CREDITO":
        saldo += valor
    elif operation == "DEBITO":
        saldo -= valor
    saldoAnterior = saldo
    listValues.append(saldo)
    for replica in listReplicas:
        enviaMsg(replica, msg)
        saldo = saldoAnterior

if __name__ == "__main__":
    main()
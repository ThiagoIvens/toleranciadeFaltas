import socket, threading

HOST = '127.0.0.1'       # Endereco IP do Servidor
USER_PORT = 1000
PORT = 1010    # Porta que o Servidor esta
saldo = 0
listReplicas = [1020, 1030, 1040, 1050]
contador_confirmados = 0

def main():
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    print("Iniciando Thread")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicia uma conexao tcp
    s.bind((HOST, USER_PORT)) # define o destino da conexao
    s.listen() # começa a escutar no destino definido
    while True:
        con, port = s.accept() # define a conexao e atribui a variavel conn, quando o servidor aceitar
        try:
            while True:
                msg = con.recv(1024)
                if not msg: break
                data = msg.decode().split('|')
                id = data[0] # atribui o primeiro valor a variavel id
                operation = data[1] # atribui o segundo valor a variavel operation
                valor = data[2] # atribui o terceiro valor a variavel valor
                
                print(data)

                if (operation == "CREDITO"):
                    saldo += valor
                    print('Cliente requisitou Crédito\nNovo saldo é de', saldo, ', enviando para comparação...')
                    msg = str(id)+'|COMPARE|CREDITO|'+str(valor)
                    for replica in listReplicas:
                        enviaMsg(replica, msg)

                elif (operation == "DEBITO"):
                    saldo -= valor
                    print('Cliente requisitou Débito\nNovo saldo é de', saldo, ', enviando para comparação...')
                    msg = str(id)+'|COMPARE|DEBITO|'+str(valor)
                    for replica in listReplicas:
                        enviaMsg(replica, msg)
                        

                elif (operation == "OK"):
                    # faz o codigo de OK
                    contador_confirmados += 1
                    
                    if contador_confirmados == 4:
                        print('Todas replicas retornaram OK')
                        enviaMsg(USER_PORT, msg)
                        contador_confirmados = 0
                    
        finally:
            print('fechou conexao')
            s.close() # fexa a conexao com o servidor
            break

def enviaMsg(port, data):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.connect((HOST, port))
    conexao.sendall(data.encode('utf-8'))


if __name__ == "__main__":
    main()
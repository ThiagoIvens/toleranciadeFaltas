import socket, threading
HOST = '127.0.0.1'       # Endereco IP do Servidor
SERVER_PORT = 7000
PORT = 3000    # Porta que o Servidor esta
listReplicas = [1000, 2000, 4000]
listValues = []

class Saldo(object):
    def __init__(self, valor):
        self._saldo = valor

class Contador(object):
    def __init__(self, valor):
        self.contador = valor

saldo = Saldo(0)
contador = Contador(0)

def main():
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    saldo._saldo
    contador.contador
    print("Iniciando Thread")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicia uma conexao tcp
    s.bind((HOST, PORT)) # define o destino da conexao
    s.listen() # começa a escutar no destino definido
    while True:
        con, port = s.accept() # define a conexao e atribui a variavel conn, quando o servidor aceitar
        msg = con.recv(1024)
        if not msg: break
        data = msg.decode().split('|')
        id = data[0] # atribui o primeiro valor a variavel id
        operation1 = data[1] # atribui o segundo valor a variavel operation
        operation2 = data[2]
        valor = int(data[3]) # atribui o terceiro valor a variavel valor
        
        print(data)

        def comparar():
                if(len(listValues) == 5):
                    for i in len(listValues):
                        if(listValues[0] != listValues[i]):
                            return False
                    return True

        def enviaMsg(port, data):
            conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conexao.connect((HOST, port))
            conexao.sendall(data)

        def codeDentrodoIF(msg, valor, operation):
            contador.contador +=1
            if operation == "CREDITO":
                saldo._saldo += valor
            elif operation == "DEBITO":
                saldo._saldo -= valor
            saldoAnterior = saldo._saldo
            listValues.append(saldo._saldo)
            for replica in listReplicas:
                enviaMsg(replica, msg)
                saldo._saldo = saldoAnterior

        if (operation1 == "COMPARE"):
            # faz o codigo de OK
            codeDentrodoIF(msg, valor, operation2)
            
            if contador.contador == 5 or len(listValues) == 5:
                if comparar:
                    print('Todas replicas retornaram OK')
                    msg = str(id)+'|OK|'+str(saldo._saldo)
                    enviaMsg(SERVER_PORT, msg)
                    contador.contador = 0
                else:
                    print('Todas replicas retornaram OK')
                    msg = str(id)+'|ERRO|'+str(saldo._saldo)
                    enviaMsg(SERVER_PORT, msg)
                    contador.contador = 0
            
            elif len(listValues) != 5 and contador.contador !=5:
                for replica in listReplicas:
                    enviaMsg(replica, msg)
                    
            print('fechou conexao')
            s.close() # fexa a conexao com o servidor

if __name__ == "__main__":
    main()
import socket, threading
HOST = '127.0.0.1'       # Endereco IP do Servidor
SERVER_PORT = 7000
PORT = 1000    # Porta que o Servidor esta
listReplicas = [2000, 3000, 4000]
listValues = []

class Saldo(object):
    def __init__(self, valor):
        self._saldo = valor

class Contador(object):
    def __init__(self, valor):
        self.contador = valor

saldo = Saldo(0)
contador = Contador(0)

def comparar():
    if(len(listValues) == 5):
        for i in len(listValues):
            if(listValues[0] != listValues[i]):
                return False
        return True
        
def testarConn(conexao, port): 
    try:
        return conexao.connect((HOST, port))
    except:
        testarConn(conexao, PORT)

def enviaMsg(port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexao:
        testarConn(conexao, port)
        conexao.sendall(data.encode('utf-8'))
        print("Mensagem enviada para a Réplica de porta: ", port)

def codeDentrodoIF(msg, valor, operation):
    print('entrou no code dentro do if')
    msg = msg.decode('utf-8')
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

def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    saldo._saldo
    contador.contador
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
                valor = int(data[3]) # atribui o terceiro valor a variavel valor
                
                print(data)

                if (operation1 == "COMPARE"):
                    print('entrou no if')
                    # faz o codigo de OK
                    codeDentrodoIF(msg, valor, operation2)
                    
                    if contador.contador == 5 or len(listValues) == 5:
                        if comparar:
                            print('Todas replicas retornaram OK!')
                            msg = str(id)+'|OK|'+str(saldo._saldo)
                            enviaMsg(SERVER_PORT, msg)
                            contador.contador = 0
                        else:
                            print('Deu ERRO no calculo!')
                            msg = str(id)+'|ERRO|'+str(saldo._saldo)
                            enviaMsg(SERVER_PORT, msg)
                            contador.contador = 0
                    
                    elif len(listValues) != 5 or contador.contador !=5:
                        contadorLista = 0
                        if(contadorLista == 3):
                            for replica in listReplicas:
                                msg = msg.decode('utf-8')
                                enviaMsg(replica, msg)
                                contadorLista += 1
        finally:
            s.close()

def main():
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

if __name__ == "__main__":
    main()
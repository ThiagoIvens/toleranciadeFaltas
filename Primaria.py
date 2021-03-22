import socket, threading

HOST = '127.0.0.1'       # Endereco IP do Servidor
PORT = 7000   # Porta que o Servidor esta
USER_PORT = 6000
listReplicas = [1000, 2000, 3000, 4000]

class Saldo(object):
    def __init__(self, valor):
        self.total = valor

class Confirmado(object):
    def __init__(self, valor):
        self.contador = valor

saldo = Saldo(0)
confirmados = Confirmado(0)

def testarConn(conexao, port): 
    try:
        return conexao.connect((HOST, port))
    except:
        testarConn(conexao, PORT)

def enviaMsg(port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexao:
        testarConn(conexao, port)
        conexao.sendall(data.encode('utf-8'))

def main():
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    print("Iniciando PRIMARIA")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicia uma conexao tcp
    s.bind((HOST, USER_PORT)) # define o destino da conexao
    s.listen() # começa a escutar no destino definido
    while True:
        con, port = s.accept() # define a conexao e atribui a variavel conn, quando o servidor aceitar
        try:
            while True:
                msg = con.recv(1024) # pega os dados recebidos e atribui a variavel msg
                if not msg: break # se msg estiver vazio para todo o processo
                data = msg.decode().split('|') # decodifica a mensagem de bytes para string e separa por |, transformando em uma lista de string
                id = data[0] # atribui o primeiro valor da lista a variavel id
                operation = data[1] # atribui o segundo valor da lista a variavel operation
                valor = int(data[2]) # atribui o terceiro valor da lista a variavel valor
                print(data)

                if operation == 'CREDITO':
                    saldo.total += valor
                    print('Cliente requisitou Crédito\nNovo saldo experado é', saldo.total, ', enviando para comparação...')
                    msg = str(id)+'|CREDITO|'+str(valor)
                    for replica in listReplicas:
                        enviaMsg(replica, msg)

                elif (operation == "DEBITO"):
                    saldo.total -= valor
                    print('Cliente requisitou Débito\nNovo saldo é de', saldo.total, ', enviando para comparação...')
                    msg = str(id)+'|DEBITO|'+str(valor)
                    for replica in listReplicas:
                        enviaMsg(replica, msg)

                elif (operation == "OK"):
                    # faz o codigo de OK
                    confirmados.contador += 1
                    print("\nCOMPARADOS ATE O MOMENTO: ",confirmados.contador)
                    if confirmados.contador == 4:
                        print('Todas replicas retornaram OK')
                        msg = str(id) + "|OK|" + str(saldo.total)
                        enviaMsg(USER_PORT, msg)
                        confirmados.contador = 0    
                        print('Fechando conexao....')
                        s.close() # fexa a conexao com o servidor

                elif (operation == "ERRO"):
                    print('ERRO')
                    msg = str(id) + '|ERRO|' + str(saldo._saldo)
                    enviaMsg(USER_PORT, msg)
                    confirmados.contador = 0    
                    print('Fechando conexao....') 
                    s.close() # fexa a conexao com o servidor
        finally:
            s.close()

if __name__ == "__main__":
    main()
import socket, threading

HOST = '127.0.0.1'       # Endereco IP do Servidor
PORT = 7000   # Porta que o Servidor esta
USER_PORT = 6000
listReplicas = [3000, 4000, 5000, 6000]

class Saldo(object):
    def __init__(self, valor):
        self._saldo = valor

class Confirmado(object):
    def __init__(self, valor):
        self._confirmado = valor

saldo = Saldo(0)
contador = Confirmado(0)

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
        
        msg = con.recv(1024) # pega os dados recebidos e atribui a variavel msg
        if not msg: break # se msg estiver vazio para todo o processo
        data = msg.decode().split('|') # decodifica a mensagem de bytes para string e separa por |, transformando em uma lista de string
        id = data[0] # atribui o primeiro valor da lista a variavel id
        operation = data[1] # atribui o segundo valor da lista a variavel operation
        valor = int(data[2]) # atribui o terceiro valor da lista a variavel valor
        print(data)
    
        if operation == 'CREDITO':
            saldo._saldo += valor
            print('Cliente requisitou Crédito\nNovo saldo é de', saldo._saldo, ', enviando para comparação...')
            msg = str(id)+'|COMPARE|CREDITO|'+str(valor)
            for replica in listReplicas:
                enviaMsg(replica, msg)

        elif (operation == "DEBITO"):
            saldo._saldo -= valor
            print('Cliente requisitou Débito\nNovo saldo é de', saldo._saldo, ', enviando para comparação...')
            msg = str(id)+'|COMPARE|DEBITO|'+str(valor)
            for replica in listReplicas:
                enviaMsg(replica, msg)

        elif (operation == "OK"):
            # faz o codigo de OK
            contador._confirmado += 1
            if contador._confirmado == 4:
                print('Todas replicas retornaram OK')
                enviaMsg(USER_PORT, msg)
                contador_confirmados = 0    
        
            print('fechou conexao')
            s.close() # fexa a conexao com o servidor
        elif (operation == "ERRO"):
            print('ERRO')
            msg = str(id)+'|ERRO|'+str(saldo._saldo)
            enviaMsg(USER_PORT, msg)
                

def enviaMsg(port, data):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.connect((HOST, port))
    conexao.sendall(data.encode('utf-8'))


if __name__ == "__main__":
    main()
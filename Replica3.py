import socket, threading
HOST = '127.0.0.1'       # Endereco IP do Servidor
SERVER_PORT = 7000
PORT = 3000    # Porta que o Servidor esta
listReplicas = [1000, 2000, 4000]
listValues = []
REPLICA = 3

class Saldo(object):
    def __init__(self, valor):
        self.total = valor

class Confirmados(object):
    def __init__(self, valor):
        self.contador = valor

saldo = Saldo(0)
confirmados = Confirmados(0)

def comparar(): # classe para comparar os valores
    if(len(listValues) == 4): # se o tamanho da lista for igual a 5
        for i in len(listValues): # para i em tamanho da lista
            if(listValues[0] != listValues[i]): # se o valor na listValues de indice 0 é igual ao o objeto da listaValues de indice i
                return False 
        return True
        
def testarConn(conexao, port):   # função para testar a conexao
    try: # tenta
        return conexao.connect((HOST, port)) # retorna a conexao
    except: # se ocorre uma exceção ao tentar executar o codigo acima faz
        testarConn(conexao, PORT) # chama a propria funçao para tentar a conexao novamente

def enviaMsg(port, data): # função para enviar o valor data para a porta informada
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexao: # com socket como conexao faz
        testarConn(conexao, port) # chama a função conexao
        conexao.sendall(data.encode('utf-8')) # envia a para conexao a mensagem em bytes
        print(data + " enviada para a Réplica de porta: ", port)
        
def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    print("Iniciando Replica", REPLICA)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicia uma conexao tcp
    s.bind((HOST, PORT)) # define o destino da conexao
    s.listen() # começa a escutar no destino definido
    while True: # loop
        con, port = s.accept() # aceita a conexao e atribui a variavel conn, e atribui a porta e host do conectado a port
        try: # tenta
            while True: # loop 
                msg = con.recv(1024) # recebe os dados de con e atribui a msg
                if not msg: break # se nao tem nada em msg, para o while
                data = msg.decode().split('|') # transforma a mensagem recebida de byte para string e separa por |
                id = data[0] # atribui o primeiro valor a variavel id
                operation = data[1] # atribui o segundo valor a variavel operation1
                valor = int(data[2]) # atribui o quarto valor a variavel valor

                if operation == "CREDITO": # se operation for igual a CREDITO
                    saldo.total += valor # soma o valor passado a saldo
                elif operation == "DEBITO": # se operation for igual a DEBITO
                    saldo.total -= valor # subtrai o valor passado a saldo
                elif operation == "COMPARE":
                    listValues.append(valor)
                    confirmados.contador += 1
                    print("\nCOMPARADOS ATE O MOMENTO: ",confirmados.contador)
                
                if confirmados.contador == 4 or len(listValues) == 4: # se o contador for igual 5 ou o tamanho da listValues for igual a 5
                    if comparar(): # executa a funçao comparar
                        print('Todas replicas retornaram OK!')
                        msg = str(id)+'|OK|'+str(saldo.total)  # define a mensagem a ser enviada
                        enviaMsg(SERVER_PORT, msg) # envia a mensagem para o servidor
                        confirmados.contador = 0 # zera o contador
                    else:
                        print('Deu ERRO no calculo!')
                        msg = str(id)+'|ERRO|'+str(saldo.total) # define a mensagem a ser enviada
                        enviaMsg(SERVER_PORT, msg) # envia a mensagem para o servidor
                        confirmados.contador = 0 # zera o contador
                else:
                    contadorLista = 0 # atribui uma variavel com atributo = 0
                    if(contadorLista < 3): # se contador for menor que 3
                        for replica in listReplicas: # para cada replica em listReplicas faz
                            msg = data[0] + "|COMPARE|" + str(saldo.total)
                            enviaMsg(replica, msg) # envia a mensagem contida na variavel msg para a replica
        finally:
            s.close() # fecha a conexao com o servidor

def main(): # classe para iniciar tudo
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

if __name__ == "__main__":
    main()
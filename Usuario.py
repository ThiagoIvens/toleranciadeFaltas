import socket, threading 

HOST = '127.0.0.1'      # ip do server
PORT = 6000             # porta
SERVER_PORT = 7000
global id;              # id das operações realizadas pelo usuario


class Saldo(object):
    def __init__(self, valor):
        self.total = valor

saldo = Saldo(0)

def main():
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima
    menuInteration() # Menu de Interação

def menuInteration():
    id = 1
    opt = input("Qual operação desejada?\n[1] Crédito\n[2] Débito\n") #mostra o menu e grava a opção em opt

    if opt == '1': # verifica se opt é igual a '1', ou seja, CREDITO
        valor= int(input("Digite o valor: ")) # pega o que o usuario digitar e atribui a variavel valor
        clientRequest = str(id) +"|CREDITO|"+str(valor) # grava a requisição do usuario com id, op, valor da requisição
        print("Enviei - ID:"+str(id)+", Operação de Crédito, e saldo igual a "+str(saldo.total))
        sendTo_Function(clientRequest.encode('utf-8')) # envia pro servidor
        id += 1
    elif opt == '2': # verifica se opt é igual a '2', ou seja, DEBITO
        valor= int(input("Digite o valor: ")) # pega o que o usuario digitar e atribui a variavel valor
        clientRequest = str(id) +"|DEBITO|"+str(valor) # grava a requisição do usuario com id, op, valor da requisição
        print("Enviei - D:"+str(id)+", Operação de Débito, e saldo igual a "+str(saldo.total))
        sendTo_Function(clientRequest.encode('utf-8')) # envia pro servidor
        id += 1
    else: # se opt for diferente de 1 e de 2 faz o codigo abaixo
        print("\nERRO: Operação inválida!\n") # printa mensagem de erro
        menuInteration() # faz a recursividade pro usuario digitar a operação desejada

def sendTo_Function(clientRequest): # função para enviar a requisição do usuario para o servidor 
     
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp: # Cria uma conexao do tipo tcp
        tcp.connect((HOST, PORT)) # conecta a conexao criada ao destino 
        tcp.sendall(clientRequest) # envia a requisição do usuario para o servidor
    
    tcp.close # fecha a conexao tcp

def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    print("Iniciando Thread")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicia uma conexao tcp
    s.bind((HOST, SERVER_PORT)) # define o destino da conexao
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
                valor = int(data[2]) # atribui o terceiro valor da lista a variavel valors

                if (operation == "OK"):
                    print('OK: Operação realizada, id ', str(id) + ' seu novo saldo é de ', str(valor) )
                    saldo.total = valor
                    print('Fechando conexao...')
                    s.close() # fexa a conexao com o servidor
                elif (operation == "ERRO"):
                    print('ERRO: Operação nao realizada, seu saldo continua ', saldo)

        finally:
            print('Fechando conexao...')
            s.close() # fexa a conexao com o servidor   

if __name__ == "__main__":
    main()
import socket, threading 

HOST = '127.0.0.1'      # ip do server
PORT = 1001             # porta
DEST = (HOST, PORT)
global id;              # id das operações realizadas pelo usuario
saldo = 0

def main():
    menuInteration() # Menu de Interação
    t = threading.Thread(target = threadOfReceived) # Define a função threadOfReceived como thread
    t.start() # Inicia a Thread acima

def menuInteration():
    id = 1
    opt = input("Qual operação desejada?\n[1] Crédito\n[2] Débito\n") #mostra o menu e grava a opção em opt

    if opt == '1': # verifica se opt é igual a '1', ou seja, CREDITO
        valor= int(input("Digite o valor: ")) # pega o que o usuario digitar e atribui a variavel valor
        clientRequest = str(id) +"|CREDITO|"+str(valor) # grava a requisição do usuario com id, op, valor da requisição
        print("Enviei - ID:"+str(id)+", Operação de Crédito, e saldo igual a "+str(saldo))
        sendTo(clientRequest) # envia pro servidor
        id += 1
    elif opt == '2': # verifica se opt é igual a '2', ou seja, DEBITO
        valor= int(input("Digite o valor: ")) # pega o que o usuario digitar e atribui a variavel valor
        clientRequest = str(id) +"|DEBITO|"+str(valor) # grava a requisição do usuario com id, op, valor da requisição
        print("Enviei - D:"+str(id)+", Operação de Débito, e saldo igual a "+str(saldo))
        sendTo(clientRequest) # envia pro servidor
        id += 1
    else: # se opt for diferente de 1 e de 2 faz o codigo abaixo
        print("\nERRO: Operação inválida!\n") # printa mensagem de erro
        menuInteration() # faz a recursividade pro usuario digitar a operação desejada

def sendTo(clientRequest): # função para enviar a requisição do usuario para o servidor 
     
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp: # Cria uma conexao do tipo tcp
        tcp.connect((HOST, PORT)) # conecta a conexao criada ao destino 
        tcp.sendall(clientRequest.encode('utf-8')) # envia a requisição do usuario para o servidor
    
    tcp.close # fecha a conexao tcp

def threadOfReceived(): # função para ficar a espera da mensagem do sevidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # inicia uma conexao tcp
    server.bind((HOST, PORT)) # define o destino da conexao
    server.listen() # começa a escutar no destino definido
    while True:
        conn = server.accept() # define a conexao e atribui a variavel conn, quando o servidor aceitar
        try:
            while True:
                s_return = conn.recv(1024) # grava em s_return o retorno do servidor
                if not s_return: break
                s_return = s_return.decode # tira a mensagem do formato binario
                s_return = s_return.split('|') # esplita os dados da mensagem por |
                id = s_return[0] # atribui o primeiro valor a variavel id
                operation = s_return[1] # atribui o segundo valor a variavel operation
                valor = s_return[2] # atribui o terceiro valor a variavel valor

                if (operation == "OK"): # verifica se a operação retornada foi OK
                    print("\nRecebi OK de operação realizada com sucesso! ID da operação: "+ str(id) + ". Saldo novo:" + str(valor)) # mostra na tela as informações retornadas
                    break
        finally:
            conn.close() # fexa a conexao com o servidor

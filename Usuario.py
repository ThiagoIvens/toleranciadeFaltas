import socket, threading 

HOST = '127.0.0.1'      # ip do server
PORT = 1000             # porta
global id;              # id das operações realizadas pelo usuario
saldo = 0

def main():
    menuInteration() # Menu de Interação

def menuInteration():
    id = 1
    opt = input("Qual operação desejada?\n[1] Crédito\n[2] Débito\n") #mostra o menu e grava a opção em opt

    if opt == '1': # verifica se opt é igual a '1', ou seja, CREDITO
        valor= int(input("Digite o valor: ")) # pega o que o usuario digitar e atribui a variavel valor
        clientRequest = str(id) +"|CREDITO|"+str(valor) # grava a requisição do usuario com id, op, valor da requisição
        print("Enviei - ID:"+str(id)+", Operação de Crédito, e saldo igual a "+str(saldo))
        sendTo_Function(clientRequest.encode('utf-8')) # envia pro servidor
        id += 1
    elif opt == '2': # verifica se opt é igual a '2', ou seja, DEBITO
        valor= int(input("Digite o valor: ")) # pega o que o usuario digitar e atribui a variavel valor
        clientRequest = str(id) +"|DEBITO|"+str(valor) # grava a requisição do usuario com id, op, valor da requisição
        print("Enviei - D:"+str(id)+", Operação de Débito, e saldo igual a "+str(saldo))
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

if __name__ == "__main__":
    main()
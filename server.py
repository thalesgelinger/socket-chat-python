import socket 
import select 
import sys 
from thread import *
  
def get_port():  
    try:
        port = int(sys.argv[1]) 
        return port
    except:
        print "PRECISA INFORMAR A PORTA!"
        exit()

def set_socket(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    HOST_NAME = socket.gethostname()
    IP_ADDRESS = socket.gethostbyname(HOST_NAME)
    
    server.bind((IP_ADDRESS, port)) 
    server.listen(100) 

    print "O servidor esta rodando em ", IP_ADDRESS , " na porta ", port

    return server

port = get_port()
server = set_socket(port)

list_of_clients = [] 
  
def clientthread(conn, addr): 

    conn.send("Bem vindo ao chat por linha de comando!") 
  
    while True: 
        try: 
            message = conn.recv(2048) 
            if message: 
                print "<" + addr[0] + "> " + message 
                message_to_send = "<" + addr[0] + "> " + message 
                broadcast(message_to_send, conn) 
            else: 
                remove(conn) 
        except: 
            continue
  
def broadcast(message, connection): 
    for client in list_of_clients: 
        if client != connection: 
            try: 
                client.send(message) 
            except: 
                client.close() 
                remove(client) 
  
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
    conn, addr = server.accept() 
    list_of_clients.append(conn) 
    print addr[0] + " se conectou"
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 

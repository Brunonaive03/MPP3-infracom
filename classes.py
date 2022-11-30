import socket
import time
import threading as th
from datetime import datetime

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_names = []
    connections = []

    def __init__(self):
        self.sock.bind(("localhost", 10000))
        self.sock.listen(2)


    def run(self):
        while len(self.connections) < 2:
            c, a = self.sock.accept()
            print(str(a[0]) + ": " + str(a[1]), "connected")
            c.send(bytes("nome", "utf-8"))
            name = c.recv(1024).decode("utf-8")

            self.client_names.append(name)
            self.connections.append(c)
            
        else:
            
            for connection in self.connections:

                for name in self.client_names:
            
                    connection.send(bytes("username" + name, "utf-8"))
                    
                time.sleep(0.05)

                connection.send(bytes("p2p", "utf-8"))

                time.sleep(0.05)

class Client_Server:


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    name = ""
    other_username = ""
    server = False
    sentMsgs = 0
    msgNum = 1

    def __init__(self, name):

        self.name = name
    
    def sendMsg(self, c):
        while True:
            date = datetime.now().strftime("%d/%m/%Y %H:%M")
            data = f'{date}: {input()}'
            c.send(bytes(data, "utf-8"))
            self.sentMsgs += 1
            print(f"{self.name} #{self.sentMsgs} enviado {data} ")
        
        

    def run(self):
        self.sock.connect(("localhost", 10000))
        while not self.server:


            try:
                data = self.sock.recv(1024)
            
                if "username".encode("utf-8") in data:
                    name = (data.removeprefix(b"username")).decode("utf-8")
                    

                    if name != self.name:
                 
                        self.other_username = name

                elif "nome".encode("utf-8") in data:
                    self.sock.send(bytes(self.name, "utf-8"))

                elif "p2p".encode("utf-8") in data:

                    self.sock.close()
                    self.server = True
                    
            except:
                break

        else:
            print("server")
            time.sleep(1)
            self.newServer()


            
    def newServer(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", 12121))
        self.sock.listen(1)

        
        not_first = False

       

        while True:
            c = self.sock.accept()[0]

            if not_first:
                c.send(bytes("received", "utf-8"))     
            not_first = True
                    
            iThread = th.Thread(target=self.sendMsg, daemon = True, args = (c,))
            iThread.start()

            while True:
                try:
                    data = c.recv(1024).decode("utf-8")
            
                    if data == "received":
                        print(f"{self.other_username} diz #{self.sentMsgs} recebida")
                    else:
                        date = datetime.now().strftime("%d/%m/%Y %H:%M")
                        print(f"{self.other_username} #{self.msgNum} (enviado {data[0:16]}h/recebido {date}h):{data[18:]}")
                        self.msgNum += 1
                        self.sock.send(bytes("received", "utf-8"))
                except:
                    break

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    name = ""
    other_username = ""
    Client2 = False
    sentMsgs = 0
    msgNum = 1

    def __init__(self, name):

        self.name = name

    def sendMsg(self):
        while True:
            date = datetime.now().strftime("%d/%m/%Y %H:%M")
            data = f'{date}: {input()}'
            self.sock.send(bytes(data, "utf-8"))

            print(f"{self.name} #[] enviado {data} ")

    def run(self):

        self.sock.connect(("localhost", 10000))
        while not self.Client2:
            try:

                data = self.sock.recv(1024)
                

                if "username".encode("utf-8") in data:
                    name = (data.removeprefix(b"username")).decode("utf-8")

                    if name != self.name:
                        
                        self.other_username = name
                        

                elif "nome".encode("utf-8") in data:
                    self.sock.send(bytes(self.name, "utf-8"))

                elif "p2p".encode("utf-8") in data:     

                    self.sock.close()
                    self.Client2 = True                            
            except:
                break
        else:
            time.sleep(1)
            self.newClient()

    def rcv(self):
        while True:
            try:

                data = self.sock.recv(1024).decode("utf-8")
             
                if data == "received":
                    print(f"{self.other_username} diz #{self.sentMsgs} recebida")
                else:
                    date = datetime.now().strftime("%d/%m/%Y %H:%M")
                    print(f"{self.other_username} #{self.msgNum} (enviado {data[0:16]}h/recebido {date}h):{data[18:]}")
                    self.msgNum += 1
                    self.sock.send(bytes("received", "utf-8"))
            except:
                break

    def newClient(self):

        while True:

            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("localhost", 12121))

            iThread = th.Thread(target=self.rcv, daemon = True)
            iThread.start()
    
            date = datetime.now().strftime("%d/%m/%Y %H:%M")
            data = f'{date}: {input()}'
            self.sock.send(bytes(data, "utf-8"))

            self.sentMsgs += 1
            print(f"{self.name} #{self.sentMsgs} enviado {data} ")
            

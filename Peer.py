import socket
import random
import threading

mainrfcdatabase = []
peerrfcdatabase = []
activepeers = []


class rfc(object):
    def __init__(self, rfcnum, title, hostname, portnum):
        self.rfcnum = rfcnum
        self.title = title
        self.hostname = hostname
        self.portnum = portnum
        self.ttl = 7200

    @staticmethod
    def get_rfc(rfcnum):
        for i in peerrfcdatabase:
            if i.ttl != 0 and i.rfcnum == rfcnum:
                return i.hostname

    @staticmethod
    def push_rfc():
        message = "P2P-DI/1.0 200 OK.\n"
        for i in peerrfcdatabase:
            if i.hostname == peerName and i.portnum == peerPort:
                message += "RFC: %s Title: %s Hostname: %s Port: %s\n" % (i.rfcnum, i.title, i.hostname, i.portnum)
        return message


class Peer(object):
    def __init__(self, hostname, portnum):
        self.hostname = hostname
        self.portnum = portnum

    @staticmethod
    def addpeer(hostname, portnum):
        activepeers.append(Peer(hostname, portnum))


class Client(threading.Thread):
    def __init__(self, peerSocket):
        threading.Thread.__init__(self)
        self.clientSocket = peerSocket
        self.running = True

    def option(self, choice):
        global serverName, serverPort, peerName, peerPort, cookie, activepeers
        if choice == 1:
            rfcpeer.register()
        elif choice == 2:
            rfcpeer.findPeers()
        elif choice == 3:
            userportnum = input("port number of the peer you want to query: ")
            rfcpeer.rfcquery(userportnum)
        # elif (choice == '4'):
        elif choice == 5:
            rfcpeer.keepalive()
        elif choice == 6:
            rfcpeer.addrfc()
            print("length of queried rfc index: %s\n" % len(peerrfcdatabase))
        elif choice == 7:
            rfcpeer.leave()
        else:
            print("Invalid Option \n")
        self.clientSocket.close()

    def run(self):
        while self.running:
            choice = input("Choose 1-7 \n 1: Register \n 2: PQuery \n 3: RFCQuery \n 4: GetRFC \n 5: KeepAlive \n 6: Add RFC's \n 7: Leave \n")
            rfcpeer.option(choice)

    def leave(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))
        message = "LEAVE P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" % (peerName, peerPort, cookie)
        self.clientSocket.send(message.encode())
        response = self.clientSocket.recv(1024).decode()
        self.clientSocket.close()

    def register(self):
        global cookie
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))
        if cookie != 0:
            message = "REGISTER P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" % (peerName, peerPort, cookie)
            self.clientSocket.send(message.encode())
            response = self.clientSocket.recv(1024).decode()

        else:
            message = "REGISTER P2P-DI/1.0 \nHostname: %s \nPort: %s" % (peerName, peerPort)
            self.clientSocket.send(message.encode())
            response = self.clientSocket.recv(1024)
            response.decode()
            line = response.splitlines()
            cookie = line[1].split()[1]
        self.clientSocket.close()

    def findPeers(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))
        message = "PQUERY P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" % (peerName, peerPort, cookie)
        self.clientSocket.send(message.encode())
        response = self.clientSocket.recv(1024).decode()
        print("print response from rs: \n%s" % response)
        peers = response.splitlines()
        self.clientSocket.close()
        del activepeers[:]
        for i in peers[:]:
                hostname = i.split()[1]
                portnum = i.split()[3]
                Peer.addpeer(hostname, portnum)
        print("number of peers in pquery %d\n" % len(activepeers))

    def keepalive(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))
        message = "KEEPALIVE P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" % (peerName, peerPort, cookie)
        self.clientSocket.send(message.encode())
        response = self.clientSocket.recv(1024).decode()
        self.clientSocket.close()

    def addrfc(self):
        for i in range(0, 60):
            rfctitle = "rfc" + str(i)
            peerrfcdatabase.append(rfc(i, rfctitle, peerName, peerPort))

    def rfcquery(self, portnum):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((peerName, portnum))
        message = "GET RFC-Index \n Hostname: %s \nPort: %s \n" % (peerName, int(peerPort))
        self.clientSocket.send(message)
        response = self.clientSocket.recv(100000)
        print("Queried RFCs: %s\n" % response)
        responseLine = response.splitlines()
        for i in responseLine[1:]:
            rfcnum = i.split()[1]
            title = i.split()[3]
            hostname = i.split()[5]
            portnum = i.split()[7]
            peerrfcdatabase.append(rfc(rfcnum, title, hostname, portnum))
        print("update length: %d" % len(peerrfcdatabase))
        self.clientSocket.close()

class Server(threading.Thread):
    def __init__(self, connectedsocket, addr):
        threading.Thread.__init__(self)
        self.connectedsocket = connectedsocket
        self.addr = addr
        self.running = True
        print("Client- " + self.addr[0] + " connected")

    def run(self):
        while (self.running):
            serverInput = self.connectedsocket.recv(1024)
            if not serverInput:
                break
            print("Started interacting with the peer %s" % peerPort)
            inputlines = serverInput.splitlines()
            if(inputlines[0].split()[0] == "GET" and inputlines[0].split()[1] == "RFC-Index"):
                print("IN SERVER")
                self.connectedsocket.send(rfc.push_rfc())

            else:
                self.connectedsocket.send("P2P-DI/1.0 404 Bad Request")

    def stop(self):
        self.running = False

peerName = socket.gethostname()
peerPort = random.randint(65000, 65200)
serverName = 'localhost'
serverPort = 65423
cookie = 0

peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerSocket.connect((serverName, serverPort))

ptpserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ptpserverSocket.bind(('', peerPort))
ptpserverSocket.listen(1)

print("Peer %s listening with port number %d" % (peerName, peerPort))

rfcpeer = Client(peerSocket)
rfcpeer.start()

while True:
    connectedSocket, addr = ptpserverSocket.accept()
    initializationThread = Server(connectedSocket, addr)
    initializationThread.start()

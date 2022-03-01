import random
import socket
import threading
from datetime import datetime

activepeerlist = []


class Peer(object):
    def __init__(self, hostname, cookie, portnum):
        self.hostname = hostname
        self.cookie = cookie
        self.flag = 1
        self.ttl = 7200
        self.portnum = portnum
        self.activecount = 1
        self.regdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def register(hostname, portnum):
        for p in activepeerlist:
            if p.hostname == hostname and p.portnum == portnum:
                p.flag = 1
                p.ttl = 7200
                p.regdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                p.activecount += 1
                print("Peer already Exists")
                message = "P2P-DI/1.0 200 OK. Peer " + p.hostname + "  is active. \nCookie: %s" % p.cookie
                return message
        cookie = random.randint(100, 1000)
        activepeerlist.append(Peer(hostname, cookie, portnum))
        print("Peer Added")
        message = "P2P-DI/1.0 200 OK. Peer Added \nCookie: %s" % cookie
        return message

    @staticmethod
    def leave(hostname, portnum):
        for p in activepeerlist:
            if p.hostname == hostname and p.portnum == portnum:
                p.flag = 0
                return "Peer on port %s has been deactivated" % portnum
        return "P2P/1.0 400 Peer not registered"

    @staticmethod
    def pquery(hostname, portnum):
        message = ""
        for p in activepeerlist:
            if p.portnum != portnum and p.flag == 1:
                message += "Hostname: " + p.hostname + " PortNumber: " + p.portnum + "\n"
            # else:
            #     continue
        return message

    @staticmethod
    def keepalive(hostname, portnum):
        for i in activepeerlist:
            if i.hostname == hostname and i.portnum == portnum:
                i.ttl = 7200
                return "TTL reset"

        return "P2P/1.0 400 Peer not registered"


class Client(threading.Thread):
    def __init__(self, connectedsocket, addr):
        threading.Thread.__init__(self)
        self.phostname = None
        self.pportnum = None
        self.connectedsocket = connectedsocket
        self.addr = addr
        self.running = True
        print("Client- " + self.addr[0] + " connected rs 71")

    def run(self):
        while self.running:
            peerInput = self.connectedsocket.recv(1024)
            if not peerInput:
                break
            inputLine = peerInput.splitlines()
            self.phostname = inputLine[1].split()[1]
            self.pportnum = inputLine[2].split()[1]
            if inputLine[0].split()[0] == "REGISTER":
                message = Peer.register(self.phostname, self.pportnum)
                self.connectedsocket.send(message)
                print("number of peers %d\n" % len(activepeerlist))

            elif (inputLine[0].split()[0] == "LEAVE"):
                message = Peer.leave(self.phostname, self.pportnum)
                self.connectedsocket.send(message)
                print("number of peers %d\n" % len(activepeerlist))

            elif (inputLine[0].split()[0] == "PQUERY"):
                message = Peer.pquery(self.phostname, self.pportnum)
                self.connectedsocket.send(message)

            elif (inputLine[0].split()[0] == "KEEPALIVE"):
                message = Peer.keepalive(self.phostname, self.pportnum)
                self.connectedsocket.send(message)

        print("Socket has been disconnected")
        self.running = False


serverName = socket.gethostname
serverPort = 65423
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The RS server is ready to receive')

while True:
    connectedSocket, addr = serverSocket.accept()
    initializationThread = Client(connectedSocket, addr)
    initializationThread.start()

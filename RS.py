import random
import socket
import threading
from datetime import datetime

activepeerlist = []


class peer(object):
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
        for i in activepeerlist:
            if i.hostname == hostname and i.portnum == portnum:
                i.flag = 1
                i.ttl = 7200
                i.regdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                i.activecount += 1
                return "Peer is active not added"

        cookie = random.randint(1, 1000)
        activepeerlist.append(peer(hostname, cookie, portnum))
        return "P2P/1.0 200 OK"

    @staticmethod
    def leave(hostname, portnum):
        for i in activepeerlist:
            if i.hostname == hostname and i.portnum == portnum:
                i.flag = 0
                return "Peer has been deactivated"

        return "P2P/1.0 400 Peer not registered"

    @staticmethod
    def pquery(hostname, portnum):
        message = ""
        for i in activepeerlist:
            if i.hostname != hostname and i.portnum != portnum and i.flag == 1:
                message += "Hostname " + i.hostname + "Port number " + i.portnum + "\n"
            else:
                continue

        return message

    @staticmethod
    def keepalive(hostname, portnum):
        for i in activepeerlist:
            if i.hostname == hostname and i.portnum == portnum:
                i.ttl = 7200
                return "TTL reset"

        return "P2P/1.0 400 Peer not registered"

    class client(threading.Thread):
        def __init__(self, connectedsocket, addr):
            self.connectedsocket = connectedsocket
            self.addr = addr
            self.running = True

        def execute(self):
            while (self.running):
                peerInput = self.connectedsocket.recv(1024)
                inputLine = recv.splitlines()
                if (inputLine[0].split()[0] == "register"):
                    self.phostname = inputLine[1].split()[1]
                    self.pportnum = inputLine[2].split()[1]
                    message = peer.register(self.phostname, self.pportnum)
                    self.connectedsocket.send(message)

                elif (inputLine[0].split()[0] == "leave"):
                    self.phostname = inputLine[1].split()[1]
                    self.pportnum = inputLine[2].split()[1]
                    message = peer.leave(self.phostname, self.pportnum)
                    self.connectedsocket.send(message)

                elif (inputLine[0].split()[0] == "pquery"):
                    self.phostname = inputLine[1].split()[1]
                    self.pportnum = inputLine[2].split()[1]
                    message = peer.pquery(self.phostname, self.pportnum)
                    self.connectedsocket.send(message)

                elif (inputLine[0].split()[0] == "keepalive"):
                    self.phostname = inputLine[1].split()[1]
                    self.pportnum = inputLine[2].split()[1]
                    message = peer.keepalive(self.phostname, self.pportnum)
                    self.connectedsocket.send(message)

            print("Socket has been disconnected")
            self.running = False

    serverName = socket.gethostname
    serverPort = 65423
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')

    while True:
        connectedSocket, addr = serverSocket.accept()
        initializationThread = client(connectedSocket, addr)
        initializationThread.start()
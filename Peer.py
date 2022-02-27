import socket
import random
import threading

rfcdatabase = []
activepeers = []

class rfc(object):
    def __init__(self, rfcnum, title, hostname, portnum):
        self.rfcnum = rfcnum
        self.title = title
        self.hostname = hostname
        self.portnum = portnum
        self.ttl = 7200

    @staticmethod
    def addrfc(rfcnum, title, hostname, portnum):
        rfcdatabase.append(rfc(rfcnum, title, hostname, portnum))
        return

    @staticmethod
    def findrfc(rfcnum):
        for i in rfcdatabase:
            if (i.ttl != 0 and i.rfcnum == rfcnum):
                return i.hostname

    @staticmethod
    def sendrfc():
        message = "P2P-DI/1.0 200 OK.\n"
        for i in rfddatabase:
            if (i.hostname == hostname and i.portnum == portnum):
                message += "RFC: %s Title: %s Hostname: %s Port: %s\n" %(i.rfcnum, i.title, i.hostname, i.portnum)
        return message


class peer(object):
    def __init__(self, hostname, portnum):
        self.hostname = hostname
        self.portnum = portnum

    @staticmethod
    def addpeer(selfhostname, portnum):
        activepeers.append(peer(hostname, portnum))


class client(threading.thread):
    def __init__(self, connectedsocket):
        self.connectedsocket = connectedsocket
        self.runnning = True

    def register(self):
        self.connectedsocket = socket.socket(socket.AF_INTE, socket.SOCK_STREAM)
        self.connectedsocket.connect(serverIp, serverPort)

        message = "register %s %s %s" % (peerName, peerPort)
        self.connectedsocket.send(message)
        response = self.connectedsocket.recv(1024)
        print(response)
        activethread = keepalive()
        activethread.start()
        self.connectedsocket.close()

    def rfcquery(self, hostname, portnum):
        self.connectedsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectedsocket.connet(hostname, portnum)
        message = "GET RFCIndex \n Hostname: %s \nPort: %s \n" % (peerName, int(peerPort))
        self.connectedsocket.send(message)
        response = self.connectedsocket.recv(4096)
        print(response)
        responseLines = response.splitLines()
        for i in responseLines[1:]:
            rfcnum = i.split()[1]
            title = i.split()[3]
            hostname = i.split()[5]
            portnum = i.split()[7]
            for j in rfcdatabase:
                if(j.rfcnum == rfcnum):
                    break
            rfc.addrfc(rfcnum, title, hostname, portnum)
        self.connectedsocket.close()

    def findrfc(self, rfcnum):
        for i in rfcdatabase:
            if (i.rfcnum == rfcnum):
                self.connectedsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connectedsocket.connect(i.hostname, int(i.portnum))
                message = "GET RFC %s\n" % (rfcnum)
                self.connectedsocket.send(message)
                response = self.connectedsocket.recv(1024)
                status = response.splitLines()
                if (status[0].split[1] != '200'):
                    print("Request error")
                    return False
                return
            else:
                continue
        print("RFC not found")
        return

    def findPeers(self):
        self.connectedsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectedsocket.connect(serverIp, serverPort)
        message = "pquery %s %s\n" % (peerName, peerPort)
        self.connectedsocket.send(message)
        response = self.connectedsocket.recv(1024)
        print(response)
        peers = response.splitLines()
        self.connectedsocket.close()
        activepeers = []
        for i in peers[1:]:
            phostname = i.split()[1]
            pportnum = i.split()[3]
            peer.addpeer(phostname, pportnum)

class server(threading.Thread):
    def __init__(self, connectedsocket, addr):
        self.connectedsocket = connectedsocket
        self.addr = addr
        self.running = True

    def execute(self):
        while (self.running):
            serverInput = self.connectedsocket.recv(1024)
            inputlines = recv.splitlines()

            if(inputLines[0].split()[0] == "GET" and inputLines[0].split()[1] == "RFCIndex"):
                self.phostname = inputLines[1].split()[1]
                self.connectsocket.send(rfc.sendrfc)
            elif(inputLines[0].split()[0]=="GET" and lines[0].split()[1]=="RFC"):
                rfcnum = inputlines[0].split()[2]
                rfcfile = path + "rfc" + rfcnum + ".txt"
                try:
                    f = open(rfcfile, 'rb')
                    self.connectedsocket.send("P2P-DI/1.0 200 OK \n")
                except IOError:
                    print("File not found")
                    self.connectedsocket.send("P2P-DI/1.0 400 Bad Request\n")
                    self.connectedsocket.shutdown(socket.SHUT_WR)
            else:
                self.connectedsocket.send("P2P-DI/1.0 404 Bad Request")

    def stop(self):
        self.running = False

class keepalive(threading.Thread):
    def __init__(self):
        self.connectedsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def execute(self):
        while (self.running):
            self.connectedsocket = socket.socket(socket.AF_INENT, socket.SOCK_STREAM)
            sleep(2000)
            self.connectedsocket.connnect(serverIp, serverPort)
            message = "keepalive P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" %(peerName, peerPort, cookie)
            self.connectedsocket.send(message)
            response = self.connectedsocket.recv(1024)
            print (response)
            self.connectedsocket.close()
    def stop(self):
        self.running = False


peerName = socket.gethostname
peerPort = random.randint(65000, 65200)
serverIp = 'localhost'
serverPort = 65423
cookie = 0

peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
serverSocket.bind('', peerPort)
serverSocket.listen(1)

print('The peer is ready to receive')

rfcpeer = client(connectedsocket, addr)
rfcpeer.execute()

while True:
    connectedsocket, addr = serverSocket.accept()
    rfcserver = server(connectedsocket, addr)
    rfcserver.execute()

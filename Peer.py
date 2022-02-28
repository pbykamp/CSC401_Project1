import socket
import random
import threading

rfcdatabase = []
activepeers = []


# class rfc(object):
#     def __init__(self, rfcnum, title, hostname, portnum):
#         self.rfcnum = rfcnum
#         self.title = title
#         self.hostname = hostname
#         self.portnum = portnum
#         self.ttl = 7200
#
#     @staticmethod
#     def addrfc(rfcnum, title, hostname, portnum):
#         rfcdatabase.append(rfc(rfcnum, title, hostname, portnum))
#         return
#
#     @staticmethod
#     def findrfc(rfcnum):
#         for i in rfcdatabase:
#             if (i.ttl != 0 and i.rfcnum == rfcnum):
#                 return i.hostname
#
#     @staticmethod
#     def sendrfc(hostname, portnum):
#         message = "P2P-DI/1.0 200 OK.\n"
#         for i in rfcdatabase:
#             if (i.hostname == hostname and i.portnum == portnum):
#                 message += "RFC: %s Title: %s Hostname: %s Port: %s\n" %(i.rfcnum, i.title, i.hostname, i.portnum)
#         return message


class Peer(object):
    def __init__(self, hostname, portnum):
        self.hostname = hostname
        self.portnum = portnum

    @staticmethod
    def addpeer(self, hostname, portnum):
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
        # elif (choice == '2'):
        #     rfcclientthread.getActivePeers()
        # elif (choice == '3'):
        #     if not temp_activePeers:
        #         print
        #         "No active peers in the network. Try contacting the RS again. \n"
        #         return
        #     for i in temp_activePeers:
        #         rfcclientthread.rfcQuery(i.host, i.port)
        # elif (choice == '4'):
        #     rfc_no = str(raw_input("Enter RFC no to be fetched: "))
        #     start = datetime.datetime.now()
        #     rfcclientthread.getRfc(rfc_no)
        #     end = datetime.datetime.now()
        #     delta = end - start
        #     print
        #     "Time taken to download all files %d msecs" % (delta.seconds * 1000 + delta.microseconds / 1000)
        # elif (choice == '5'):
        #     self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     self.c_socket.connect((serverip, serverport))
        #     msg2send = "LEAVE P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" % (peername, peerport, cookie)
        #     self.c_socket.send(msg2send)
        #     recv = self.c_socket.recv(1024)
        #     print
        #     recv
        #     self.c_socket.close()
        else:
            print("Wrong Input. Choose 1-5 \n")
        self.clientSocket.close()

    def run(self):
        while self.running:
            choice = input("Enter choice(1-5) \n 1: Register with RS \n 2: Get Active Peer list from RS \n 3: Get RFC index of Peers \n 4: Get RFC from Peer \n 5: Leave P2P network \n")
            print(choice)
            rfcpeer.option(choice)

    def register(self):
        global cookie
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))
        if cookie != 0:
            print("HERE NOT NOT 0")
            message = "REGISTER P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" % (peerName, peerPort, cookie)
            self.clientSocket.send(message)
            response = self.clientSocket.recv(1024)
            print("printing response: %s" % response)
            # activethread = keepalive()
            # activethread.start()

        else:
            print("HERE 0")
            message = "REGISTER P2P-DI/1.0 \nHostname: %s \nPort: %s" % (peerName, peerPort)
            self.clientSocket.send(message)
            print("HERE 1")
            response = self.clientSocket.recv(1024)
            print("printing response 112: %s" % response)
            line = response.splitlines()
            cookie = line[1].split()[1]
            # activethread = keepalive()
            # activethread.start()
        self.clientSocket.close()

    # def rfcquery(self, hostname, portnum):
    #     self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.clientSocket.connet(hostname, portnum)
    #     message = "GET RFCIndex \n Hostname: %s \nPort: %s \n" % (peerName, int(peerPort))
    #     self.clientSocket.send(message)
    #     response = self.clientSocket.recv(4096)
    #     print(response)
    #     responseLine = response.splitlines()
    #     for i in responseLine[1:]:
    #         rfcnum = i.split()[1]
    #         title = i.split()[3]
    #         hostname = i.split()[5]
    #         portnum = i.split()[7]
    #         for j in rfcdatabase:
    #             if(j.rfcnum == rfcnum):
    #                 break
    #         rfc.addrfc(rfcnum, title, hostname, portnum)
    #     self.connectedsocket.close()

    # def findrfc(self, rfcnum):
    #     for i in rfcdatabase:
    #         if (i.rfcnum == rfcnum):
    #             self.connectedsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             self.connectedsocket.connect(i.hostname, int(i.portnum))
    #             message = "GET RFC %s\n" % (rfcnum)
    #             self.connectedsocket.send(message)
    #             response = self.connectedsocket.recv(1024)
    #             status = response.splitLines()
    #             if (status[0].split[1] != '200'):
    #                 print("Request error")
    #                 return False
    #             return
    #         else:
    #             continue
    #     print("RFC not found")
    #     return

    # def findPeers(self):
    #     self.connectedsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.connectedsocket.connect(serverName, serverPort)
    #     message = "pquery %s %s\n" % (peerName, peerPort)
    #     self.connectedsocket.send(message)
    #     response = self.connectedsocket.recv(1024)
    #     print(response)
    #     peers = response.splitLines()
    #     self.connectedsocket.close()
    #     activepeers = []
    #     for i in peers[1:]:
    #         phostname = i.split()[1]
    #         pportnum = i.split()[3]
    #         Peer.addpeer(phostname, pportnum)


# class server(threading.Thread):
#     def __init__(self, connectedsocket, addr):
#         self.connectedsocket = connectedsocket
#         self.addr = addr
#         self.running = True
#
#     def execute(self):
#         while (self.running):
#             serverInput = self.connectedsocket.recv(1024)
#             inputlines = serverInput.splitlines()
#
#             if(inputlines[0].split()[0] == "GET" and inputlines[0].split()[1] == "RFCIndex"):
#                 self.phostname = inputlines[1].split()[1]
#                 self.connectsocket.send(rfc.sendrfc)
#             elif(inputlines[0].split()[0]=="GET" and inputlines[0].split()[1]=="RFC"):
#                 rfcnum = inputlines[0].split()[2]
#                 rfcfile = path + "rfc" + rfcnum + ".txt"
#                 try:
#                     f = open(rfcfile, 'rb')
#                     self.connectedsocket.send("P2P-DI/1.0 200 OK \n")
#                 except IOError:
#                     print("File not found")
#                     self.connectedsocket.send("P2P-DI/1.0 400 Bad Request\n")
#                     self.connectedsocket.shutdown(socket.SHUT_WR)
#             else:
#                 self.connectedsocket.send("P2P-DI/1.0 404 Bad Request")
#
#     def stop(self):
#         self.running = False

# class keepalive(threading.Thread):
#     def __init__(self):
#         self.connectedsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.running = True
#
#     def execute(self):
#         while (self.running):
#             self.connectedsocket = socket.socket(socket.AF_INENT, socket.SOCK_STREAM)
#             # sleep(200)
#             self.connectedsocket.connnect(serverName, serverPort)
#             message = "keepalive P2P-DI/1.0 \nHostname: %s \nPort: %s \nCookie: %s" % (peerName, peerPort, cookie)
#             self.connectedsocket.send(message)
#             response = self.connectedsocket.recv(1024)
#             print(response)
#             self.connectedsocket.close()
#
#     def stop(self):
#         self.running = False


peerName = socket.gethostname()
peerPort = random.randint(65000, 65200)
serverName = 'localhost'
serverPort = 65423
cookie = 0

path = "/Users/pujithapolimetla/PycharmProjects/CSC401_Project1/rfc"

peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerSocket.connect((serverName, serverPort))
# serverSocket = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
# serverSocket.bind('', peerPort)
# serverSocket.listen(1)

print("Peer Server is listening on %s with port number %d" % (peerName, peerPort))

rfcpeer = Client(peerSocket)
rfcpeer.start()

# while True:
#     connectedsocket, addr = serverSocket.accept()
#     rfcserver = server(connectedsocket, addr)
#     rfcserver.execute()

import random
import socket
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

        cookie = random.randint(1,1000)
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
    def query(hostname, portnum):
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



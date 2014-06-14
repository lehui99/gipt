import json
import socket
from threading import Thread
import time
import random
import sys
import socks

class ProxySocket(object):

    def __init__(self, config, socksProxy):
        self.config = config
        if type(socksProxy) == int:
            self.host = config['defaultSocksHost']
            self.port = socksProxy
        else:
            self.host = socksProxy[0]
            self.port = socksProxy[1]
        self.failCount = 0
        self.fail = False

    def __cmp__(self, another):
        return self.failCount - another.failCount

    def apply(self, socksocket):
        socksocket.set_proxy(socks.SOCKS5, self.host, self.port)

class CheckProxies(Thread):

    def __init__(self, config):
        Thread.__init__(self)
        self.daemon = True
        self.config = config

    def run(self):
        while True:
            for socksProxy in self.config['socksProxies']:
                s = socks.socksocket()
                socksProxy.apply(s)
                s.settimeout(self.config['socketTimeout'])
                try:
                    s.connect(('www.google.com', 80))
                    s.send(bytearray(b'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'))
                    if s.recv(65536) == '':
                        raise Exception()
                    socksProxy.fail = False
                except Exception:
                    socksProxy.failCount += 1
                    socksProxy.fail = True
            time.sleep(self.config['checkInterval'])

class ProxySelector(object):

    def __init__(self, config):
        self.config = config

    def __call__(self):
        goodProxies = [socksProxy for socksProxy in self.config['socksProxies'] if not socksProxy.fail]
        goodProxies.sort()
        return goodProxies[int(random.randint(0, len(goodProxies)) * random.randint(0, len(goodProxies)) / len(goodProxies)) - 1]

class Pipe(Thread):

    def __init__(self):
        Thread.__init__(self)

    def setSockPair(self, sockIn, sockOut):
        self.sockIn = sockIn
        self.sockOut = sockOut

    def pipeData(self):
        try:
            while True:
                data = self.sockIn.recv(65536)
                if data == '':
                    break
                self.sockOut.send(data)
        finally:
            self.sockIn.close()
            self.sockOut.close()

    def run(self):
        self.pipeData()

class Tunnel(Pipe):

    def __init__(self, config, sock, hosts, proxySelector):
        Pipe.__init__(self)
        self.config = config
        self.sock = sock
        self.hosts = hosts
        self.proxySelector = proxySelector

    def run(self):
        proxySock = socks.socksocket()
        self.proxySelector().apply(proxySock)
        host = self.hosts[random.randint(0, len(self.hosts) - 1)]
        proxySock.connect((host[0], host[1]))
        pipe = Pipe()
        pipe.setSockPair(proxySock, self.sock)
        pipe.start()
        self.setSockPair(self.sock, proxySock)
        self.pipeData()

class Server(Thread):

    def __init__(self, config, port, hosts, proxySelector):
        Thread.__init__(self)
        self.config = config
        self.hosts = hosts
        self.proxySelector = proxySelector
        self.sock = socket.socket()
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(50)

    def run(self):
        #tunnels = []
        while True:
            clientSock, clientAddr = self.sock.accept()
            tunnel = Tunnel(self.config, clientSock, self.hosts, self.proxySelector)
            tunnel.start()
            #tunnels.append(pipe)

class Main(object):

    def __init__(self, config):
        config['socksProxies'] = [ProxySocket(config, socksProxy) for socksProxy in config['socksProxies']]
        self.config = config

    def start(self):
        CheckProxies(self.config).start()
        #servers = []
        proxySelector = ProxySelector(self.config)
        for k, v in self.config['tunnelServers'].items():
            server = Server(self.config, int(k), v, proxySelector)
            server.start()
            #servers.append(tunnel)

if __name__ == '__main__':
    Main(json.loads(open(sys.argv[1], 'r').read())).start()

import json
import logging
try:
    from gevent import socket
    from gevent import Greenlet as Concurrent
except ImportError:
    import socket
    from threading import Thread as Concurrent
    print('Cannot find gevent, using threading')
import time
import random
import sys

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

    def __lt__(self, another):
        return self.failCount < another.failCount

    def connect(self, socksocket, address):
        socksocket.connect((self.host, self.port))
        socksocket.send(b'\x05\x01\x00')
        if socksocket.recv(1) != b'\x05':
            raise Exception('Not a socks5 proxy')
        if socksocket.recv(1) != b'\x00':
            raise Exception('Socks5 proxy has no non-authentication method')
        addrStr = chr(len(address[0])) + str(address[0]) + chr(int(address[1] / 0x100)) + chr(int(address[1] % 0x100))
        try:
            socksocket.send(b'\x05\x01\x00\x03' + addrStr.encode('iso-8859-1'))
        except UnicodeDecodeError:
            socksocket.send(b'\x05\x01\x00\x03' + addrStr)
        if socksocket.recv(1) != b'\x05':
            raise Exception('Not a socks5 proxy')
        if socksocket.recv(1) != b'\x00':
            raise Exception('Proxy cannot connect to remote host')
        socksocket.recv(1)
        atyp = socksocket.recv(1)

        def recvFully(socksocket, count):
            while count > 0:
                l = len(socksocket.recv(count))
                if l == 0:
                    raise Exception('EOF Exception')
                count -= l

        if atyp == b'\x01':
            recvFully(socksocket, 4)
        elif atyp == b'\x03':
            addrLen = ord(socksocket.recv(1))
            recvFully(socksocket, addrLen)
        elif atyp == b'\x04':
            recvFully(socksocket, 16)
        else:
            raise Exception('Not recognize socks5 atyp')
        recvFully(socksocket, 2)
        logging.debug('Connectted through %s to %s.', str((self.host, self.port)), str(address))

class CheckProxies(Concurrent):

    def __init__(self, config):
        Concurrent.__init__(self)
        self.daemon = True
        self.config = config

    def run(self):
        while True:
            for socksProxy in self.config['socksProxies']:
                s = socket.socket()
                s.settimeout(self.config['checkTimeout'])
                try:
                    socksProxy.connect(s, ('www.google.com', 80))
                    s.send(bytearray(b'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'))
                    data = s.recv(65536)
                    if data == b'' or data == '' or data == None:
                        raise Exception()
                    socksProxy.fail = False
                    logging.debug('Proxy %s is alive.', (socksProxy.host, socksProxy.port))
                except Exception:
                    socksProxy.failCount += 1
                    socksProxy.fail = True
                    logging.debug('Proxy %s is dead.', (socksProxy.host, socksProxy.port))
                finally:
                    s.close()
            time.sleep(self.config['checkInterval'])

    def _run(self):
        self.run()

class ProxySelector(object):

    def __init__(self, config):
        self.config = config

    def __call__(self):
        goodProxies = [socksProxy for socksProxy in self.config['socksProxies'] if not socksProxy.fail]
        goodProxies.sort()
        return goodProxies[int(random.randint(0, len(goodProxies)) * random.randint(0, len(goodProxies)) / len(goodProxies)) - 1]

class Pipe(Concurrent):

    def __init__(self):
        Concurrent.__init__(self)

    def setSockPair(self, sockIn, sockOut):
        self.sockIn = sockIn
        self.sockOut = sockOut

    def pipeData(self):
        try:
            while True:
                data = self.sockIn.recv(65536)
                if data == b'' or data == '' or data == None:
                    break
                self.sockOut.send(data)
        except Exception:
            logging.info('Pipe end')
        finally:
            self.sockIn.close()
            self.sockOut.close()

    def run(self):
        self.pipeData()

    def _run(self):
        self.run()

class Tunnel(Pipe):

    def __init__(self, config, sock, hosts, proxySelector):
        Pipe.__init__(self)
        self.config = config
        self.sock = sock
        self.hosts = hosts
        self.proxySelector = proxySelector

    def run(self):
        try:
            proxySock = socket.socket()
            self.sock.settimeout(self.config['socketTimeout'])
            host = self.hosts[random.randint(0, len(self.hosts) - 1)]
            self.proxySelector().connect(proxySock, (host[0], host[1]))
            pipe = Pipe()
            pipe.setSockPair(proxySock, self.sock)
            pipe.start()
            self.setSockPair(self.sock, proxySock)
            self.pipeData()
        except Exception:
            logging.exception('Exception in Tunnel:')
        finally:
            self.sock.close()
            proxySock.close()

class Server(Concurrent):

    def __init__(self, config, port, hosts, proxySelector):
        Concurrent.__init__(self)
        self.config = config
        self.hosts = hosts
        self.proxySelector = proxySelector
        self.sock = socket.socket()
        try:
            self.sock.bind(('0.0.0.0', port))
            self.sock.listen(50)
        except Exception:
            logging.exception('Exception in Server init:')
            raise

    def run(self):
        #tunnels = []
        while True:
            try:
                clientSock, clientAddr = self.sock.accept()
                clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                tunnel = Tunnel(self.config, clientSock, self.hosts, self.proxySelector)
                tunnel.start()
                logging.debug('Accepted connection from %s.', str(clientAddr))
                #tunnels.append(pipe)
            except Exception:
                logging.exception('Exception in Server run:')

    def _run(self):
        self.run()

class Main(object):

    def __init__(self, config):
        logging.basicConfig(filename = config['logFilename'], level = getattr(logging, config['logLevel']))
        config['socksProxies'] = [ProxySocket(config, socksProxy) for socksProxy in config['socksProxies']]
        self.config = config

    def start(self):
        CheckProxies(self.config).start()
        servers = []
        proxySelector = ProxySelector(self.config)
        for k, v in self.config['tunnelServers'].items():
            server = Server(self.config, int(k), v, proxySelector)
            server.start()
            servers.append(server)
        for server in servers:
            server.join()

if __name__ == '__main__':
    Main(json.loads(open(sys.argv[1], 'r').read())).start()

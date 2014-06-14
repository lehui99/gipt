import json
import socket
from threading import Thread
import time
import sys
import socks

class ProxySocket(object):

    def __init__(self, config, socksProxy):
        if type(socksProxy) == int:
            self.host = config['defaultSocksHost']
            self.port = socksProxy
        else:
            self.host = socksProxy[0]
            self.port = socksProxy[1]

    def apply(self, socksocket):
        socksocket.set_proxy(socks.SOCKS5, self.host, self.port)

class CheckProxies(Thread):

    def __init__(self, config):
        Thread.__init__(self)
        self.config = config

    def run(self):
        while True:
            for socksProxy in self.config['socksProxies']:
                pass
            time.sleep(self.config['checkInterval'])

class Main(object):

    def __init__(self, config):
        self.config = config
        config['socksProxies'] = [ProxySocket(config, socksProxy) for socksProxy in config['socksProxies']]

    def start(self):
        CheckProxies(self.config).start()

if __name__ == '__main__':
    Main(json.loads(open(sys.argv[1], 'r').read())).start()

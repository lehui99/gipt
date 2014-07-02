import re
import base64
import os
try:
    import urllib.request as urlProc
except:
    import urllib as urlProc

if __name__ == '__main__':
    qrIter = re.finditer(b"'(media/qr/\\d+.png)'", urlProc.urlopen('https://www.shadowsocks.net/get').read())
    ssUrls = set()
    for qr in qrIter:
        qrUrl = b'http://zxing.org/w/decode?u=' + (b'https://www.shadowsocks.net/' + qr.group(1)).replace(b':', b'%3A').replace(b'/', b'%2F')
        try:
            ssUrlIter = re.finditer(b'ss://(.*?)<', urlProc.urlopen(qrUrl.decode('iso-8859-1')).read())
            for ssUrl in ssUrlIter:
                ssUrls.add(ssUrl.group(1) + b'==')
        except Exception:
            print('Error process ' + qrUrl)
    i = 1
    for ssUrl in ssUrls:
        ssInfo = base64.b64decode(ssUrl)
        idx = ssInfo.index(b'@')
        ssAuth = ssInfo[ : idx]
        ssHost = ssInfo[idx + 1 : ]
        idx = ssAuth.index(b':')
        ssMethod = ssAuth[ : idx]
        ssPasswd = ssAuth[idx + 1 : ]
        idx = ssHost.index(b':')
        ssServer = ssHost[ : idx]
        ssServerPort = ssHost[idx + 1 : ]
        ssCfgFile = open('..' + os.sep + 'ss' + str(i) + 'config.json', 'w')
        ssCfgFile.write('''{
    "server":"%s",
    "server_port":%s,
    "local_port":%d,
    "password":"%s",
    "timeout":600,
    "method":"%s"
}
''' % (ssServer.decode('iso-8859-1'), ssServerPort.decode('iso-8859-1'), 1080 + i, ssPasswd.decode('iso-8859-1'), ssMethod.decode('iso-8859-1')))
        ssCfgFile.flush()
        ssCfgFile.close()
        i += 1

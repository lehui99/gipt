import re
import base64
import os
try:
    import urllib.request as urlProc
except:
    import urllib as urlProc

if __name__ == '__main__':
    # qrIter = re.finditer('"(media/qr/\\d+.png)"', str(urlProc.urlopen('https://www.shadowsocks.net/get').read()))
    ssUrls = set()
    ssUrls = {'YWVzLTI1Ni1jZmI6cWF6d3N4QHAuZ2FsZGIubmV0OjgwMjA==', 'cmMyLWNmYjpBa3VtQW5nZWxANjUuMTgxLjEyMC4yMDo1NjkwMg==', 'YWVzLTI1Ni1jZmI6a2lyYWtpcmFANjkuMTYzLjQwLjEyNDo4Mzg4==', 'YWVzLTI1Ni1jZmI6anVzdGZvcmZ1bkA1LjIzMS42Mi4xOTg6ODk4MQ==', 'YWVzLTI1Ni1jZmI6c2hhZG93c29ja3MubmV0QDIzLjIyNi4yMzEuMjAyOjIwODI==', 'dGFibGU6YWswLnR3QDE5OC4yMy4xODcuMTQ1OjI1ODYy==', 'cmM0OmhpZ29ANjMuMjIzLjY0LjEwMjo4ODg4==', 'YWVzLTI1Ni1jZmI6d3Ffc2hhZG93c29ja3NAMjE2LjE4OS41Ni4zNDo4MDgw==', 'YWVzLTI1Ni1jZmI6Z2FtZXNAMTA3LjE4My4xNC4xMTM6NDQz==', 'dGFibGU6ZmFrZXJwd0AyMDkuMTQxLjUxLjU4OjIwNDA2==', 'YWVzLTI1Ni1jZmI6ZmtnZndnb2dvZ29AMTkyLjI0MS4xOTkuMTYzOjEwMjQ==', 'YWVzLTI1Ni1jZmI6c2hhZG93c29ja3MubmV0QVNBQDE5Mi4zLjE4LjkxOjIzMzMz==', 'YWVzLTI1Ni1jZmI6cmF1bGhvdUAxOTIuMjQzLjExNy4yMzY6ODM4OA==', 'YWVzLTI1Ni1jZmI6bWFydGluMTIzQDEyOC4xOTkuMjA2LjE5NjoxMDUw==', 'YWVzLTI1Ni1jZmI6aGVsbG93b3JsZDIwMTRAMjMuMjQ1LjI2LjExMjo4MDkw==', 'YWVzLTI1Ni1jZmI6Z2FtZXNAMTA3LjE3MC4yMDcuNDA6OTk1==', 'YWVzLTI1Ni1jZmI6MjAxNHBhc3MhQDUuMjMxLjYwLjkzOjgwODA==', 'YWVzLTI1Ni1jZmI6Zmx5YmJzLnJ1QDEwNy4xNTAuMjguMTc2OjE5OTM==', 'YWVzLTI1Ni1jZmI6djJleEAxMDYuMTg2LjEyNC4zNzo5OTk5==', 'dGFibGU6ZGFpZ2VuZXR3b3JrQDUuMjMxLjY1LjM0Ojg4OA==', 'YWVzLTI1Ni1jZmI6MDYwNEAyMy4yMjYuMjI0LjIxNTo0NDM==', 'YmYtY2ZiOiFyZW5ydWZlaSFAMTkyLjIyNy4yMzIuMjUyOjgyMzQ==', 'YWVzLTI1Ni1jZmI6bmIxMm5iODQ1NUAxOTguMjMuMjQzLjQyOjg5ODk==', 'YWVzLTI1Ni1jZmI6V09jYW9OSU1BZGVHRldANjkuMTYzLjM3LjE0ODo0NDM=='}
    '''for qr in qrIter:
        qrUrl = 'http://zxing.org/w/decode?u=' + ('https://www.shadowsocks.net/' + qr.group(1)).replace(':', '%3A').replace('/', '%2F')
        try:
            ssUrlIter = re.finditer('ss://(.*?)<', str(urlProc.urlopen(qrUrl).read()))
            for ssUrl in ssUrlIter:
                ssUrls.add(ssUrl.group(1) + '==')
        except Exception:
            print('Error process ' + qrUrl)'''
    i = 1
    for ssUrl in ssUrls:
        ssInfo = base64.b64decode(ssUrl).decode('iso-8859-1')
        idx = ssInfo.index('@')
        ssAuth = ssInfo[ : idx]
        ssHost = ssInfo[idx + 1 : ]
        idx = ssAuth.index(':')
        ssMethod = ssAuth[ : idx]
        ssPasswd = ssAuth[idx + 1 : ]
        idx = ssHost.index(':')
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
''' % (ssServer, ssServerPort, 1080 + i, ssPasswd, ssMethod))
        ssCfgFile.flush()
        ssCfgFile.close()
        i += 1

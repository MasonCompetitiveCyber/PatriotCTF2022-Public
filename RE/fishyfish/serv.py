import sys
import socketserver

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print('Connected by', self.request)
        while True:
            try:
                req = self.request
                uid = req.recv(1024)
            except:
                break
            if not uid:
                break
            print(uid)
            if uid == b"obese dragonfish":
                data = open("./fishchecker", "rb").read()
                req.sendall(data)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    host, port = 'localhost', 10015

    sys.stderr.write('Listening {}:{}\n'.format(host, port))
    server = ThreadedTCPServer((host, port), RequestHandler)
    ThreadedTCPServer.allow_reuse_address = True
    ThreadedTCPServer.allow_reuse_port = True
    server.serve_forever()
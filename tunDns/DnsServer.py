import datetime
import sys
import time
import threading
import traceback
import SocketServer
from dnslib import *


class DomainName(str):
    def __getattr__(self, item):
        return DomainName(item + '.' + self)


D = DomainName('a.pch')
IP = '192.168.2.45'
TTL = 60 * 5
PORT = 53






def dns_response(data):
    request = DNSRecord.parse(data)
    print request
    qname = request.q.qname
    reply = DNSRecord(DNSHeader(id=request.header.id,qr=1,aa=1,ra=1),q=request.q)
    reply.add_answer(RR(rname=qname,rdata=A(IP)))
    print "---- Reply:\n", reply

    return reply.pack()


class BaseRequestHandler(SocketServer.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print "\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
                                               self.client_address[1])
        try:
            data = self.get_data()
            print len(data), data.encode('hex')  # repr(data).replace('\\x', '')[1:-1]
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):

    def get_data(self):
        data = self.request.recv(8192).strip()
        sz = int(data[:2].encode('hex'), 16)
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        sz = hex(len(data))[2:].zfill(4).decode('hex')
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


if __name__ == '__main__':
    print "Starting nameserver..."

    servers = [
        SocketServer.ThreadingUDPServer(('', PORT), UDPRequestHandler),
        SocketServer.ThreadingTCPServer(('', PORT), TCPRequestHandler),
    ]
    for s in servers:
        thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print "%s server loop running in thread: %s" % (s.RequestHandlerClass.__name__[:3], thread.name)

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        for s in servers:
            s.shutdown()
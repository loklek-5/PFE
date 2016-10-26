import SimpleHTTPServer
import SocketServer
PORT= 8080
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("192.168.2.45",PORT),Handler)
print "serving at port", PORT
httpd.serve_forever()
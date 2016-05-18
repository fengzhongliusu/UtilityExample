import threading
import sys
import time
import tornado.web
import tornado.ioloop
import tornado.websocket

class SocketHandler(tornado.websocket.WebSocketHandler):
	clients = []
	def check_origin(self, origin):
		return True

	def open(self):
		print "new connection..."
		self.write_message('welcome to Websocket')
		SocketHandler.clients.append(self)

	@classmethod
	def write_to_clients(cls):
		print "Writing to all clients..."
		if not cls.clients:
		    print "empty...."
		for client in cls.clients:
			if not client.ws_connection.stream.socket:
				print "Web socket does not exist anymore!!!"
				cls.clients.remove(client)
			else:
				client.write_message('Hi, there!')

class ServerThread(threading.Thread):
	def run(self):
		print "start server.."
		app = tornado.web.Application([
			('/soc', SocketHandler)
		])
		app.listen(8070)
		try:
			tornado.ioloop.IOLoop.instance().start()
		except KeyboardInterrupt:
			sys.exit()


if __name__ == '__main__':
	server_t = ServerThread()
	server_t.start()
	while 1:
		SocketHandler.write_to_clients()
		time.sleep(2)

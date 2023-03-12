from socket import SHUT_RDWR
import jsock
from tbroLib.Output import Output
import time
import threading

# TCP json communications module
# Uses async TCP commands to reduce number of python threads
# Spawns a watchdog thread to auto reconnect


class Comms:
	msg_in=[] # store json messages received
	connected=False
	client_sock=None
	host_port=None
	def __init__(self,host_IP:str,host_ports:int,output:Output,key,watchdog_time):
		self.output=output
		self.host_IP=host_IP
		self.host_ports=host_ports
		self.key=key
		output.assignTCP(self)
		self.watchdog_thread=threading.Thread(target=self.watchdog,args=(watchdog_time,),daemon=True)
		self.watchdog_thread.start()
	def watchdog(self,ping_delay):
		while(True):
			time.sleep(ping_delay)
			self.send({"PING":None})
			if not self.connected:
				self.output.write("WARN",f"TCP connection lost, reconnecting",False)
				self.connect()
	def receive(self):
		if self.connected:
			try:
				data=self.client_sock.receive()
				if not data is None:
					self.msg_in.insert(0,data)
			except:
				pass
		return self.available()
	def available(self):
		return len(self.msg_in)
	def read(self):
		if self.available():
			return self.msg_in.pop()
		else:
			raise Exception("Nothing to read")
	def send(self,msg,retry=True):
		if self.connected:
			try:
				self.client_sock.send(msg)
			except:
				if retry:
					self.send(msg,False)
				else:
					self.connected=False

class CommsServer(Comms):
	server_sock=None
	def create_socket(self):
		self.server_sock=jsock.ServerSocket(self.key)
		self.client_sock=self.server_sock.accept()
	def bind(self,port):
		self.output.write("INFO",f"TCP server awaiting connections at {self.host_IP}:{port}",False)
		try:
			self.server_sock.bind(self.host_IP,port)
			return True
		except Exception as e:
			self.output.write("EXCEPT",e)
			return False
	def connect(self):
		try:
			self.create_socket()
			for port in self.host_ports:
				if self.bind(port):
					self.host_port=port
					break
			while not self.connected:
				self.client_sock=self.server_sock.accept()
				self.connected=(not self.client_sock is None) and self.client_sock.poll()
				if self.connected:
					self.output.write("INFO",f"TCP client connected from {self.client_sock.remote_address} via port {self.host_port}",False)
		except Exception as e:
			self.output.write("EXCEPT",e,False)
			self.connected=False
			self.output.write("ERROR","No TCP client connected",False)
		
	def close(self):
		self.output.write("INFO","Closing sockets",True)
		try:
			if not self.server_sock is None:
				self.server_sock._socket.shutdown(SHUT_RDWR)
				self.server_sock.close()
			if not self.client_sock is None:
				self.client_sock._socket.shutdown(SHUT_RDWR)
				self.client_sock.close()
			self.client_sock=None
			self.server_sock=None
			self.connected=False
			self.output.write("INFO","Sockets Closed",False)
		except Exception as e:
			self.output.write("ERROR","Failed to close sockets",False)
			self.output.write("EXCEPT",e,False)

class CommsClient(Comms):
	def create_socket(self):
		self.client_sock=jsock.ClientSocket(self.key)
	def conn(self,port):
		self.client_sock._socket.settimeout(1)
		self.output.write("STATUS",f"Trying connection on TCP port:{port}",False)
		try:
			self.client_sock.connect(self.host_IP,port)
			return True
		except Exception as e:
			# self.output.write("EXCEPT",e)
			return False
	def connect(self):
		self.output.write("INFO",f"Connecting to TCP server at {self.host_IP}",False)
		while not self.connected:
			for port in self.host_ports:
				self.create_socket()
				if self.conn(port):
					self.host_port=port
					self.connected=self.client_sock.poll()
					self.send({"PING":None})
					if self.connected:
						break
		self.output.write("INFO",f"Connected to TCP server at {self.host_IP}:{self.host_port} from {self.client_sock.local_address}",False)
	def close(self):
		self.output.write("INFO","Closing sockets",True)
		try:
			if not self.client_sock is None:
				self.client_sock._socket.shutdown(SHUT_RDWR)
				self.client_sock.close()
			self.client_sock=None
			self.connected=False
			self.output.write("INFO","Sockets Closed",False)
		except Exception as e:
			self.output.write("ERROR","Failed to close sockets",False)
			self.output.write("EXCEPT",e,False)
	
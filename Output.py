from colorama import Fore

class typeSettings:
	def __init__(self,colour,show):
		self.colour=colour
		self.show=show

# output class for printing to terminal and over TCP
class Output:
	comms=None
	msg_types={
		"TCP"    :typeSettings(Fore.CYAN,True), ## gets replaced by tcp_name 
		"INFO"   :typeSettings(Fore.GREEN,True),
		"WARN"   :typeSettings(Fore.YELLOW,True),
		"ERROR"  :typeSettings(Fore.RED,True),
		"EXCEPT" :typeSettings(Fore.MAGENTA,True),
		"MCU"    :typeSettings(Fore.BLUE,True),
		"PING"	 :typeSettings(Fore.LIGHTBLACK_EX,True),
		"ACK"	 :typeSettings(Fore.LIGHTMAGENTA_EX,True),
		"STATUS" :typeSettings(Fore.LIGHTGREEN_EX,True),
		"RC"	 :typeSettings(Fore.LIGHTBLUE_EX,True),
	}
	def __init__(self,tcp_name):
		self.tcp_name=tcp_name
	def assignTCP(self,comms):
		self.comms=comms
	def write(self,prefix:str,msg:str,tcp=False):
		msg=str(msg)
		# Send over TCP if that is enabled for this message
		if tcp:
			try:
				self.comms.send({prefix:msg}) # formatted as a JSON key:val pair
			except:
				pass
		# Only print if enabled for that msg type
		display=True
		for type,settings in self.msg_types.items():
			if type in prefix or type in msg:
				if not settings.show:
					display=False
		if display:
			if prefix=="TCP":
				prefix=self.tcp_name
			print(self.colorise(f"{prefix.ljust(6)}: {msg}"))
		

	def toggleDisplayTypes(self,types,enabled):
		for type in types:
			if type in self.msg_types:
				self.msg_types[type].show=enabled
			else:
				self.write("ERROR",f"Message type {type} not found")

	def colorise(self,msg:str):
		for type,settings in self.msg_types.items():
			if type=="TCP":
				prefix=self.tcp_name
			else:
				prefix=type
			msg=msg.replace(prefix,settings.colour+prefix+Fore.WHITE)
		return msg
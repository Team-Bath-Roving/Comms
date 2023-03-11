# from classes.Comms import Comms

from colorama import Fore
from enum import Enum



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
		# Only print if enabled for that msg type
		if prefix in self.msg_types:
			if self.msg_types[prefix].show==True:
				print(self.colorise(f"{prefix.ljust(6)}: {msg}"))
		# Send over TCP if that is enabled for this message
		if tcp:
			try:
				self.comms.send({prefix:msg}) # formatted as a JSON key:val pair
			except:
				pass

	def toggleDisplayType(self,type,enabled):
		if type in self.msgTypes:
			self.msgTypes[type].show=enabled
		else:
			self.write("ERROR",f"Message type {type} not found")

	def colorise(self,msg:str):
		for type,settings in self.msg_settingss.items():
			if "TCP" in settings:
				settings=self.tcp_name
			msg=msg.replace(type,settings.colour+type+Fore.WHITE)
		return msg
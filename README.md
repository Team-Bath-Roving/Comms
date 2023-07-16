# Comms
Python classes for TCP comms and console output
## Overview
The Comms module allows the creation of asynchronous TCP clients and servers, which send and recieve dictionary objects via a FIFO queue at each end.  
A watchdog thread is spawned to automatically reset the connection if it is lost, and switch ports if a port is busy.  
The [jsock](https://github.com/turicas/jsock) library is used to convert the dictionary object to JSON and send it over the socket.
## Output
This class provides a way for other modules to output to the console, optionally sending over TCP as well.  
Messages are categorized, allowing the output to be filtered, e.g. to only show errors.  
Messages can also have a hierarchy, allowing the source to be determined (e.g. `TCP: MCU: INFO: Initialised` is an info message sent from the microcontroller over serial to the Pi, which has been forwarded over TCP to Misson Control.

import getopt   # getopt.getopt()
import select   # select()
import socket   # socket.socket(), obj.setblocking(), obj.bind(), obj.listen()
import sys
import Queue

target_address = ('localhost',10002)
air_address = ('localhost',10003)

target_queue = Queue.Queue()
air_queue = Queue.Queue()

target_connection = None
air_connection = None

def handle_target_data():
    # Do stuff

def handle_air_data():
    # Do sftuff

def main(argv):
    # Create a TCP/IP socket
    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target.setblocking(0)

    air = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    air.setblocking(0)

    # Bind the socket to the port
    target.bind(target_address)
    air.bind(air_address)

    # Listen for a single client on each port
    target.listen(1)
    air.listen(1)

    # Create arguments for select()
    inputs = [target, air]
    outputs = []
    
    

    while inputs:
        readable, writable, exceptional = select.select(inputs,outputs,inputs)

        # Handle inputs
        for sock in readable:
            if target and sock is target:
                target_connection, target_address = sock.accept()
                target_connection.setblocking(0)
                inputs.remove(target)
                inputs.append(target_connection)
            elif air and sock is air:
                air_connection, target_address = sock.accept()
                air_connection.setblocking(0)
                inputs.remove(air)
                inputs.append(air_connection)
            elif target_connection and sock is target_connection:
                # Get the data from the target detection subsystem
            elif air_connection and sock is air_connection:
                # Get the data from the air quality subsystem

                



if __name__ == "__main__":
    main(sys.argv[1:])

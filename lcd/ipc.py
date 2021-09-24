import threading
from main import LCDData

#### IPC ####

def listen_handler(port_number,handle_function):
    # Create a TCP/IP Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(1)
    server.bind(('localhost',port_number))
    server.listen(1)

    server_socket, client_address = server.accept()
    server_socket.setblocking(1)

    server.close()

    # Call the handler
    handle_function(server_socket)

def handle_target_data(target_socket):
    # Read in the latest image

def handle_air_data(air_socket):
    # Read in the latest temperature

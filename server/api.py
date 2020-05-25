import logging


logger = logging.getLogger("server")

def parse(data, from_socket):
    # TODO: separate parser from api
    # First 2 bytes of each packed indicate packet length in bytes. Range (0 - 65535) bytes.
    # Next 1 byte is the request ID. (0-255)
    # Next 1 byte is the status code. (0-255)
    ...

def handshake(packet, client_sock):
    # First 3 bytes - protocol version - in format MAJOR.MINOR.PATCH
    status = 0
    if len(packet) != 3 * 8:
        return 129
    int.from_bytes(packet)
    ...
    


# def send(client):...
# # def callback_request():...
# def broadcast():...
# def send_deltas(n, client):...
#     """send n number of last game events to the client"""


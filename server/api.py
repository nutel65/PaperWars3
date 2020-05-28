import logging
import statuscode
import binascii


logger = logging.getLogger("server")

# First 2 bytes of each packed indicate packet length in bytes. Range (0 - 65535) bytes.
# Next 1 byte is the request ID. (0-255)
# Next 1 byte is the status code. (0-255)

def pack(status, data):
    ...


def unpack(sock):
    packet = sock.recv(4096)
    data_len = int(packet[0])
    status = int(packet[1])
    data = int(packet[2:])
    return status, data


def handshake(packet, client_sock):
    # First 3 bytes - protocol version - in format MAJOR.MINOR.PATCH
    print("packet", packet)
    print("packet len:", len(packet))
    if len(packet) != 3:
        print("handshake not passed")
        status = statuscode.PROTOCOL_NOT_SUPPORTED
    else:
        major = packet[0]
        minor = packet[1]
        patch = packet[2]
        print(f"Client version {major}.{minor}.{patch}")
        status = statuscode.HANDSHAKE_OK
        data = binascii.a2b_hex(format(status, '02x'))
        client_sock.sendall(data)
    return status
    
    


# def send(client):...
# # def callback_request():...
# def broadcast():...
# def send_deltas(n, client):...
#     """send n number of last game events to the client"""


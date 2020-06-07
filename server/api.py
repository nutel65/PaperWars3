import logging
from server import statuscode
from server import utility

logger = logging.getLogger("server")

def handle(pack_id, status, data):
    """API for logged user."""
    # TODO: handle api call
    logger.debug(f"API call: {pack_id}, {status}, {data}")
    print(data)

# First 2 bytes of each packed indicate packet length in bytes. Range (0 - 65535) bytes.
# Next 1 byte is the request ID. (0-255)
# Next 1 byte is the status code. (0-255)


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
        client_sock.sendall(utility.int_to_bhex(status))
    return status


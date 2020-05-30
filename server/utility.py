import binascii
import config
import logging
import msgpack

logger = logging.getLogger("server")

def pack_data(status, data):
    ...


def bhex_to_int(bhex):
    # b"\x80\x80"
    tmp = binascii.b2a_hex(bhex)
    # b"8080"
    s = tmp.decode("ascii")
    # "8080"
    result = int(s, 16)
    # 32896
    return result

def int_to_bhex(integer):
    return binascii.a2b_hex(format(integer, "02x"))


def id_gen(prefix=""):
    i = 1
    while True:
        yield f"{prefix}{i}"
        i += 1

def setup_logger(name, filename="lastrun.log"):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=f'./server/logs/{filename}',
                        filemode='w+')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(config.LOGGER_LEVEL)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def exchange(sock, msg):
    # if len(active_connections) < 2:
    #     active_connections.append(sock)
    #     logger.info("Connected")
    # else:
    #     logger.warning("Refused connection. Maximum client amount reached")
    logger.info("retrieving data from socket ...")
    data = sock.recv(1024)
    logger.info(f"data received: {data}")
    msg = input("input message:\n>")
    sock.sendall(bytes(msg, "utf-8"))
    # active_connections.remove(sock)

def fetch(key, selector):
    """Download packet from read-ready socket and save data in key.data"""
    sock = key.fileobj
    if key.data["data"]:
        logger.warning(f"Buffer not empty yet: {len(key.data['data'])} bytes left. Stopped fetch.")
        return
    packet = sock.recv(config.RECV_SIZE)
    if not packet:
        selector.unregister(sock)
        sock.close()
        logger.info(f"Client closed connection")
        return -1
    try:
        head = packet[:4]
    except IndexError:
        logger.warning(f"Invalid header in packet: {packet}")
        return -1
    total_length, pack_id, status = parsehead(head)
    key.data["pack_id"] = pack_id
    key.data["status"] = status
    key.data["data"] = packet[4:]
    while len(key.data["data"]) < total_length:
        packet = sock.recv(config.RECV_SIZE)
        if not packet:
            selector.unregister(sock)
            sock.close()
            logger.info(f"Client suddenly closed connection")
            return -1
        else:
            key.data["data"] += packet
            logger.debug(f"Additional packet received: {packet}")
    if len(key.data["data"]) != total_length:
        logger.warning(f"PACKET LENGHT DO NOT MATCH ({len(key.data['data'])}/{total_length})")

def lastpack(key):
    """Return fetched data (pack_id, status, data) from key.data and clear it then."""
    if not key.data["data"]:
        raise ValueError("Key data is not available. You may want to fetch() first")
        return -1
    pack_id = key.data.get("pack_id")
    status = key.data.get("status")
    # TODO: handle invalid data passed to unpackb
    data = msgpack.unpackb(key.data.get("data"))
    key.data["pack_id"] = None
    key.data["status"] = None
    key.data["data"] = b""
    return pack_id, status, data

# First 2 bytes of each packed indicate packet length in bytes. Range (0 - 65535) bytes.
# Next 1 byte is the request ID. (0-255)
# Next 1 byte is the status code. (0-255)

def add_header(request_id, status, data_b):
    len_b = binascii.a2b_hex(format(len(data_b), '04x'))
    request_id_b = binascii.a2b_hex(format(request_id, '02x'))
    status_b = binascii.a2b_hex(format(status, '02x'))
    return len_b + request_id_b + status_b + data_b

def parsehead(header):
    """Returns: packet length, request ID, status code.""" # b'\x00\x04\x01\x05'
    if len(header) != 4:
        raise ValueError("Header must have length of 4.")
    else:
        length = int(binascii.b2a_hex(header[0:2]), 16)
        req_id = header[2]
        status = header[3]
        return length, req_id, status

def print_handles(selector):
        handles = dict(selector.get_map())
        print("HANDLES LIST:")
        for key, h in handles.items():
            print(f"[{key}: data={h.data} events={h.events}]")
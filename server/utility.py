import logging
import binascii


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



def parsehead(header):
    """Returns: packet length, request ID, status code."""
    if len(header) != 4:
        raise ValueError("Header must have length of 4.")
    else:
        return header[0], 

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
    console.setLevel(logging.INFO)
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
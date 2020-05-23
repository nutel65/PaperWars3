import logging


def id_gen(prefix=""):
    i = 1
    while True:
        yield f"{prefix}{i}"
        i += 1

def setup_logger():
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./server/logs/lastrun.log',
                        filemode='w+')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("server").addHandler(console)
    return logging.getLogger("server")


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
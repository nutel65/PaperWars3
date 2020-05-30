import api
import config
import logging
import msgpack
import selectors
import servercli
import statuscode
import threading
import time
import traceback
import utility
from collections import deque

logger = logging.getLogger("server")

class ThreadWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exitflag = 0
        self.name = "ThreadWorker"
        self.daemon = False

    def wrap_run():
        pass

    def run(self):
        logger.info(f"{self.name} service started.")
        self.wrap_run()
        logger.info(f"{self.name} service stopped.")

    def stop(self):
        self.exitflag = 1

    def status(self):
        message = f"{self.name} NOT WORKING"
        if self._check_if_alive():
            message = f"{self.name} OK"
        print(message)

    def _check_if_alive(self):
        self.join(timeout=0.0)
        return self.is_alive()


class PacketReceiver(ThreadWorker):
    # TODO: extract logged and unlogged methods out of class
    def __init__(self, selector):
        ThreadWorker.__init__(self)
        self.name = "PacketReceiver"
        self.selector = selector
        
    def wrap_run(self):
        while not self.exitflag:
            # select sockets with incoming data
            events = self.selector.select(timeout=config.SELECTOR_TIMEOUT)
            for key, mask in events:
                print("events:", events)
                if key.data["type"] == "listener":
                    self.accept_client(key)
                elif key.data["type"] == "no_handshake":
                    self.handshake_client(key)
                elif key.data["type"] == "unlogged":
                    self.handle_unlogged(key)
                elif key.data["type"] == "logged":
                    self.handle_logged(key, mask)
                else:
                    raise ValueError(f"Invalid register type: {key.data['type']}")
            
    def accept_client(self, key):
        """Accept incoming connection and and register him in selector."""
        listening_sock = key.fileobj
        client_sock, addr = listening_sock.accept()
        client_sock.setblocking(False)
        events = selectors.EVENT_READ #| selectors.EVENT_WRITE
        self.selector.register(client_sock, events, 
            data={
                "type": "no_handshake",
                "ip": addr[0],
                "port": addr[1],
                "data": b"",
                })
        logger.info(f"Client connected ({addr[0]}:{addr[1]})")


    def handshake_client(self, key):
        sock = key.fileobj
        packet = sock.recv(config.RECV_SIZE)
        print(packet)
        status = api.handshake(packet, sock)
        if status == statuscode.HANDSHAKE_OK:
            key.data["type"] = "unlogged"
        else:
            self.selector.unregister(sock)
            sock.close()
        logger.info(f"{status}")
    

    def handle_unlogged(self, key):
        """Handle unlogged client which should
        try to log in or register at this point"""
        utility.fetch(key)
        pack_id = status = data = None
        test1 = None
        # try:
        pack_id, status, data = utility.lastpack(key)
        print("1", pack_id, status, data)
        # except ValueError:
        #     pass
        print("2", pack_id, status, data)
        api.handle(pack_id, status, data)
        print("unpacked data:", msgpack.unpackb(data))
        

    def handle_logged(self, key, mask):
        """Handled client is logged at this point,
        and can send any valid api request."""
        utility.fetch(key)
        pack_id = status = data = None
        try:
            pack_id, status, data = utility.lastpack(key)
            api.handle(key, pack_id, status)
        except ValueError:
            pass

    def get_handles(self):
        handles = dict(self.selector.get_map())
        print("HANDLES LIST:")
        for key, h in handles.items():
            print(f"[{key}: data={h.data} events={h.events}]")


class CLIService(ThreadWorker):
    def __init__(self):
        ThreadWorker.__init__(self)
        self.name = "CLI"

    def wrap_run(self):
        while not self.exitflag:
            try:
                inp = input()
                servercli.exe(inp)
            except:
                logger.error(f"An error occured during command execution:\n{traceback.format_exc()}")


class DBManager(ThreadWorker):
    def __init__(self, database=None):
        ThreadWorker.__init__(self)
        self.database = database
        self.query_queue = deque()
        self.name = "DBManager"

    def wrap_run(self):
        while not self.exitflag or self.query_queue:
            if self.query_queue:
                ...
                # TODO: Add real database.
                # database.query(query_queue.popleft()) 
                print(self.query_queue.popleft())
            else:
                time.sleep(1)

    def stop(self):
        self.exitflag = 1
        if self.query_queue:
            logger.info(f"{self.name}: waiting for finishing pending queries...")

    def query(self, query_string):
        if self.exitflag:
            logger.error(f"{self.name} stopped; Could not add new query")
            return
        if not query_string:
            print("query string cannot be empty")
        self.query_queue.append(query_string)
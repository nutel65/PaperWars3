from server import api
from server import config
import logging
import msgpack
import selectors
from server import servercli
from server import statuscode
import threading
import time
import traceback
from server import utility
import psycopg2

from collections import deque

logger = logging.getLogger(__name__)

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
    def __init__(self, user, password, database, host="127.0.0.1", port="5432"):
        ThreadWorker.__init__(self)
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.query_queue = deque()
        self.name = "DBManager"

    def run(self):
        logger.info(f"{self.name} service started.")
        while not self.exitflag:
            try:
                self.connection = psycopg2.connect(user=self.user,
                                            password=self.password,
                                            host=self.host,
                                            port=self.port,
                                            database=self.database)

                self.cursor = self.connection.cursor()
                # Print PostgreSQL Connection properties
                # logger.info(self.connection.get_dsn_parameters())

                # Print PostgreSQL version
                self.cursor.execute("SELECT version();")
                record = self.cursor.fetchone()
                logger.info(f"{self.name} connected - {record}\n")
                self.wrap_run()
            except (Exception, psycopg2.Error) as error :
                logger.error(f"PostgreSQL: {error}")
            finally:
                logger.info(f"{self.name} service stopped.")
                if(self.connection):
                    self.cursor.close()
                    self.connection.close()
                    logger.info("PostgreSQL connection is closed")
            
    def wrap_run(self):
        while not self.exitflag or self.query_queue:
            if self.query_queue:
                query = query_queue.popleft()
                logger.debug(f"{self.name} executing query: {query}")
                cursor.execute(query)
            else:
                time.sleep(1)

    def stop(self):
        self.exitflag = 1
        if self.query_queue:
            logger.info(f"{self.name}: waiting for finishing pending queries...")

    def query(self, query_string):
        if self.exitflag:
            logger.warning(f"{self.name} stopped; Adding new query anyway...")
        if not query_string:
            logger.warning("Query string cannot be empty")
        self.query_queue.append(query_string)
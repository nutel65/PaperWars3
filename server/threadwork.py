import os
import time
import logging
import selectors
import traceback
import threading
from collections import deque

import psycopg2

from server import servercli


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
    def __init__(self, database_url="postgres://postgres:rafix@localhost:5432/postgres"):
        ThreadWorker.__init__(self)
        self.database_url = os.getenv('DATABASE_URL', database_url)
        self.query_queue = deque()
        self.results = {}
        self.name = "DBManager"

    def run(self):
        logger.info(f"{self.name} service started.")
        sleeptime = 3
        while not self.exitflag:
            self.connection = None
            try:
                self.connection = psycopg2.connect(self.database_url)
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
                # Print PostgreSQL Connection properties
                # logger.info(self.connection.get_dsn_parameters())
                # Print PostgreSQL version
                self.cursor.execute("SELECT version();")
                record = self.cursor.fetchone()
                logger.info(f"{self.name} connected - {record}\n")
                sleeptime = 3
                self.wrap_run()
            except (psycopg2.Error):
                logger.error(f"{self.name} Error: \n{traceback.format_exc()}")
                logger.info(f"Attempting database reconnect in {sleeptime} seconds")
                time.sleep(sleeptime)
                sleeptime *= 1.05
            finally:
                if(self.connection):
                    self.cursor.close()
                    self.connection.close()
                    logger.info("PostgreSQL connection is closed")
            logger.info(f"{self.name} service stopped.")
            
    def wrap_run(self):
        # TODO: non blocking queries
        while not self.exitflag or self.query_queue:
            try:
                if self.query_queue:
                    entry = self.query_queue.popleft()
                    query = entry.get("query")
                    args = entry.get("query_args")
                    returns = entry.get("returns")
                    callback_event = entry.get("callback_event")
                    if returns and not callback_event:
                        logger.error("should supply callback event when awaiting result")
                        return
                    logger.debug(f"{self.name} executing query: {query} with args: {args}")
                    self.cursor.execute(query, args)
                    if returns:
                        returned = self.cursor.fetchall()
                        self.results[callback_event] = returned
                        logger.debug(f"query returned: {returned}")
                    if callback_event:
                        callback_event.set()
                    logger.debug(self.cursor.statusmessage)
                else:
                    # TODO: REPLACE THAT UGLY THING BELOW
                    time.sleep(1)
            except psycopg2.errors.UniqueViolation:
                logger.debug(f"Tried inserting username that already exists")

    def stop(self):
        self.exitflag = 1
        if self.query_queue:
            logger.info(f"{self.name}: waiting for finishing pending queries...")

    def insert_user(self, username, password, privilege):
        # TODO: check if username is already taken
        entry = {
            "query": "INSERT INTO users (username, password, privilege) VALUES (%s, %s, %s)",
            "query_args": [username, password, privilege],
            "returns": False,
            "callback_event": None,
        }
        self.query_queue.append(entry)

    def get_user_by_username(self, username):
        event = threading.Event()
        entry = {
            "query": "SELECT username, password, privilege FROM users WHERE username = %s",
            "query_args": [username,],
            "returns": True,
            "callback_event": event,
        }
        logger.debug(f"get_user_by_username query (username: {username}")
        self.query_queue.append(entry)
        event.wait()
        query_result = self.results.pop(event)[0]
        logger.debug(f"get_user_by_username query returned with result: {query_result}")
        return query_result

    def select(self, query):
        event = threading.Event()
        entry = {
            "query": query,
            "query_args": [],
            "returns": True,
            "callback_event": event,
        }
        self.query_queue.append(entry)
        event.wait()
        query_result = self.results.pop(event)
        return query_result



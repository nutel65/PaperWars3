import logging
import os

logger = logging.getLogger("server")

COMMANDS = {
    "exit": "exits server",
    "help": "list commands",
}

def exe(command):
    """executes server CLI command"""
    if command not in COMMANDS:
        logger.warning("Unsupported command. Type 'help' to list commands.")
    elif command == "exit":
        logger.info("exit command execute; stopping services")
        os._exit(0)
    elif command == "help":
        print(COMMANDS)

        
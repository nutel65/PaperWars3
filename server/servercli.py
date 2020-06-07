import logging
import os
from server import utility

logger = logging.getLogger("server")

services = None
selector = None
COMMANDS = {
    "exit": "stops and safely terminates all server services",
    "exitf": "force stops program execution, exits immediately",
    "help": "list available commands",
    "dbmanager": "database manager",
    "packrec": "packet receiver",
    "handles": "lists all handles/connections"
}

def set_services(services_dict):
    global services
    services = services_dict

def set_selector(selector_obj):
    global selector
    selector = selector

def undefined_command(command=""):
    print("UNDEFINED COMMAND", command)


def exe(command):
    """executes server CLI command"""
    # if command not in COMMANDS:
    #     logger.warning("Unsupported command. Type 'help' to list commands.")
    if not(selector and command):
        raise Exception("selector or command not set")
        return
    cmd = command.split()
    if not cmd or not services:
        return
    if cmd[0] == "help":
        print()
        for command, describtion in COMMANDS.items():   
            print(f"{command.ljust(15)}{describtion}")
    elif cmd[0] == "exit":
        logger.info("exit command execute; stopping services...")
        for service in services.values():
            service.stop()
    elif cmd[0] == "exitf":
        logger.warning("exitf command execute; force stopped")
        os._exit(0)
    elif cmd[0] == "dbmanager":
        if len(cmd) == 1:
            print("dbmanager arguments: status, query")
        elif cmd[1] == "status":
            services["dbmanager"].status()
        elif cmd[1] == "query":
            services["dbmanager"].query(" ".join(cmd[2:]))
        else:
            undefined_command()
    elif cmd[0] == "packrec":
        if len(cmd) == 1:
            print("packrec arguments: status")
        elif cmd[1] == "status":
            services["packrec"].status()
        else:
            undefined_command()
    elif cmd[0] == "handles":
        # TODO: print list of connections / connected users
        # utility.print_handles(selector)
        ...
    else:
        undefined_command()
    
        
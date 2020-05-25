import logging
import os

logger = logging.getLogger("server")

services = None
active_sockets = None
COMMANDS = {
    "exit": "stops and exits server",
    "help": "list available commands",
    "dbmanager": "database manager"
}

def set_services(services_dict):
    global services
    services = services_dict

def set_active_sockets(active_sockets_list):
    global active_sockets
    active_sockets = active_sockets_list

def undefined_command(command=""):
    print("UNDEFINED COMMAND", command)


def exe(command):
    """executes server CLI command"""
    # if command not in COMMANDS:
    #     logger.warning("Unsupported command. Type 'help' to list commands.")
    cmd = command.split()
    if cmd[0] == "help":
        print(COMMANDS)
    elif cmd[0] == "exit":
        logger.info("exit command execute; stopping services")
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
    else:
        undefined_command()
    
        
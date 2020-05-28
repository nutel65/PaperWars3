import logging
import os

logger = logging.getLogger("server")

services = None
COMMANDS = {
    "exit": "stops and safely terminates all server services",
    "exitf": "force stops program execution, exits immediately",
    "help": "list available commands",
    "dbmanager": "database manager",
    "packrec": "packet receiver"
}

def set_services(services_dict):
    global services
    services = services_dict

def undefined_command(command=""):
    print("UNDEFINED COMMAND", command)


def exe(command):
    """executes server CLI command"""
    # if command not in COMMANDS:
    #     logger.warning("Unsupported command. Type 'help' to list commands.")
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
            print("packrec arguments: status, handles")
        elif cmd[1] == "status":
            services["packrec"].status()
        elif cmd[1] == "handles":
            services["packrec"].get_handles()
        else:
            undefined_command()
    else:
        undefined_command()
    
        
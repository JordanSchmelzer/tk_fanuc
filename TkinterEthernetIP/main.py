import json
import logging
import logging.config
import logging.handlers
import pathlib
import tkinter as tk
import atexit
from pycomm3 import LogixDriver


FANUC_CONTROLLER_ADDR = "10.0.0.1"
FANUC_CONTROLLER_PORT = 5001
FANUC_KAREL_TURN_90DEG_LEFT = "turnLeft()"


logger = logging.getLogger("logs/app.log")


# configure high quality, parsable, multi-destination, blocking logging
def configure_logging() -> None:
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
        
    logging.config.dictConfig(config)
    
    #
    # queue_handler = logging.getHandlerByName("queue_handler")
    # if queue_handler is not None:
    #    queue_handler.listener.start()
    #    atexit.register(queue_handler.listener.stop)
    #
    #  add this to config as root handler. you need python 3.12. I get error on 3.11
    #  "queue_handler": {
    #  "class": "logging.handlers.QueueHandler",
    #  "handlers": [
    #    "stderr",
    #    "file_json"
    #  ],
    #  "respect_handler_level": true
    # }


def main():
    configure_logging()
    create_window()


def on_button_click():
    logger.info("Button was clicked!")    
    

def create_window():
    window = tk.Tk()
    window.title("logging example interface")
    window.geometry('500x500')
    
    button = tk.Button(window, text="Click to Start", command=on_button_click)
    button.grid(column=1,row=2)
    button.pack()
    window.mainloop()


if __name__ == "__main__":
    main()
    
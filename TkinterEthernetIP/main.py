import json
import logging
import logging.config
import logging.handlers
import pathlib
#import tkinter as tk
import customtkinter as ctk
import atexit
from pycomm3 import LogixDriver
# import faroc


# tk labels: format = type_name
global label_last_log


FANUC_CONTROLLER_ADDR = "10.0.0.1"
FANUC_CONTROLLER_PORT = 5001
FANUC_KAREL_TURN_90DEG_LEFT = "turnLeft()"


PATH_TO_LOG = "logs/app.log.jsonl"
logger = logging.getLogger(PATH_TO_LOG)


# configure high quality, parsable, multi-destination, blocking logging
def configure_logging() -> None:
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
        
    logging.config.dictConfig(config)
    
    # this only works in 3.12. make this non-blocking
    # queue_handler = logging.getHandlerByName("queue_handler")
    # if queue_handler is not None:
    #    queue_handler.listener.start()
    #    atexit.register(queue_handler.listener.stop)
    #
    #  add this to config as root handler.
    #  "queue_handler": {
    #  "class": "logging.handlers.QueueHandler",
    #  "handlers": [
    #    "stderr",
    #    "file_json"
    #  ],
    #  "respect_handler_level": true
    # }


def main() -> None:
    configure_logging()
    create_window()


def on_button_click() -> None:
    logger.info("Button was clicked!")    
    update_label()
    

def update_label() -> None:
    latest_log = read_latest_log(PATH_TO_LOG)
    label_last_log.configure(text=latest_log)


def read_latest_log(file_path: str) -> dict:
    latest_log = None
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = json.loads(line)
            latest_log = log_entry
    return latest_log


def create_window() -> None:
    app = ctk.CTk()
    app.title("logging example interface")
    app.geometry('500x500')
    
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('green')
    
    button = ctk.CTkButton(master=app, text="Click to Start", command=on_button_click)
    button.grid(column=1,row=2)
    button.pack()
    
    global label_last_log
    label_last_log = ctk.CTkLabel(master=app, text="press to see latest label")
    label_last_log.pack()w    

    app.mainloop()


if __name__ == "__main__":
    main()
    
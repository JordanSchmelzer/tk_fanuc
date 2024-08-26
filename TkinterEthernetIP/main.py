# -*- coding: utf-8 -*-
"""
Created on 25AUG2024
@author: Jordan Schmelzer
demo shows how to use python classes to read and write to robot via FAROC_SERVER
demo shows how to read and write to LogiX PLC controllers
demo shows how to log 
"""

import json
import logging
import logging.config
import logging.handlers
import pathlib
import customtkinter as ctk
from faroc.faroc import FaRoC_Reader
# import atexit # 3.12 only
from pycomm3 import LogixDriver


# ----------------------------- globals --------------------------------------#
global label_last_log
global label_read_logiX
global label_flip_bit_logiX
global label_faroc_read
global label_faroc_write


# ----------------------------- constants -----------------------------------#
FANUC_CONTROLLER_ADDR = "10.0.0.1"
FANUC_CONTROLLER_PORT = 5001
FANUC_KAREL_TURN_90DEG_LEFT = "turnLeft()"
LOGIX_PLC_ADDR = "192.168.1.2"
PATH_TO_LOG = "logs/app.log.jsonl"


# --- configure high quality, parsable, multi-destination, blocking logging -----#
logger = logging.getLogger(PATH_TO_LOG)


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


# ----------------------------- Button Logic ---------------------------------------- #
def handle_click_button_show_log() -> None:
    update_log_label()
    

def update_log_label() -> None: 
    latest_log = read_latest_log(PATH_TO_LOG)
    label_last_log.configure(text=latest_log)


def read_latest_log(file_path: str) -> dict:
    latest_log = None
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = json.loads(line)
            latest_log = log_entry
    return latest_log


def handle_click_button_flip_bit(tag="default_tag"):
    try:
        tag_value = read_logiX_tag(tag)
        if tag_value:
            write_logiX_tag("default_tag",False)
        else:
            write_logiX_tag("default_tag",True)
    except Exception as e:
        logger.error(e)


def handle_click_button_read_tag(tag="default_tag"):
    try:
        tag_value = read_logiX_tag("default_tag")
        label_read_logiX.configure(tag_value)
    except Exception as e:
        logger.error(e)
        update_log_label()


# ---------------------------- logiX Controller Manipulation ------------------------------------- #
def read_logiX_tag(tag_name="default_tag"):
    plc_ip = LOGIX_PLC_ADDR 

    try:
        # Create a connection to the PLC
        with LogixDriver(plc_ip) as plc:
            # Read a tag
            tag_value = plc.read(tag_name)
            logger.info(f'Tag Value: {tag_value.value}')
            return tag_value.value
    except Exception as e:
        logging.error(f'{e}')
        update_log_label()
    

def write_logiX_tag(tag_name="DefaultTag",tag_value=True):
    plc_ip = LOGIX_PLC_ADDR

    try:
        # Create a connection to the PLC
        with LogixDriver(plc_ip) as plc:
            # Write to a tag
            success = plc.write(tag_name, tag_value)
            if success:
                logger.info(f'Success; Tag Written: {tag_name}; Tag Value: {tag_value}')
            else:
                logger.warn(f'Fail; Tag {tag_name} Not Writte; Failed Update Tag Value: {tag_value}')
    except Exception as e:
        logging.error(f'{e}')
    

# ------------------------------- FaRuc System R 30iB Controller manipulation --------------#
robot = FaRoC_Reader


def read_fanuc_controller():
    ...
    

def write_fanuc_controller():
    ...


# ------------------------------ main program --------------------------------------- #
def setup_app() -> None:
    app = ctk.CTk()
    app.title("logging example interface")
    app.geometry('500x500')
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('green')
    

    # Create frames to hold button label pairs
    frame_logs = ctk.CTkFrame(master=app)
    frame_read_logiX = ctk.CTkFrame(master=app)
    frame_write_logiX = ctk.CTkFrame(master=app)
    frame_write_faroc = ctk.CTkFrame(master=app)
    frame_read_faroc = ctk.CTkFrame(master=app)


    # Create buttons and labels
    global label_last_log
    button_update_logs = ctk.CTkButton(master=frame_logs, text="Get latest log message", width=100,command=handle_click_button_show_log)
    label_last_log = ctk.CTkLabel(master=frame_logs, text=". . .")

    global label_read_logiX
    button_read_logiX = ctk.CTkButton(master=frame_read_logiX, text="Read LogiX PLC register", width=100, command=read_logiX_tag)    
    label_read_logiX = ctk.CTkLabel(master=frame_read_logiX, text=". . .")

    global label_flip_bit_logiX
    button_flip_bit_logiX = ctk.CTkButton(master=frame_write_logiX, text="Flip Bit LogiX PLC register", width=100, command=handle_click_button_flip_bit)
    label_flip_bit_logix = ctk.CTkLabel(master=frame_write_logiX, text=". . .")

    global label_faroc_read
    button_read_faroc = ctk.CTkButton(master=frame_write_faroc, text="Get Fanuc Register", width=100, command="")
    label_read_faroc= ctk.CTkLabel(master=frame_write_faroc, text=". . .")
    
    global label_faroc_write
    button_write_faroc = ctk.CTkButton(master=frame_read_faroc, text="Write Fanuc Register", width=100, command="")
    label_write_faroc = ctk.CTkLabel(master=frame_read_faroc, text=". . .")


    # Pack elements to their respective frames
    button_update_logs.pack(side="left", padx=10, pady=10)
    label_last_log.pack(side='left',padx=10, pady=10)

    button_read_logiX.pack(side="left",padx=10, pady=10)
    label_read_logiX.pack(side="left", padx=10, pady=10)

    button_flip_bit_logiX.pack(side="left",padx=10, pady=10)
    label_flip_bit_logix.pack(side="left", padx=10, pady=10)

    button_read_faroc.pack(side="left", padx=10, pady=10)
    label_read_faroc.pack(side="left", padx=10, pady=10)
    
    button_write_faroc.pack(side="left",padx=10,pady=10)
    label_write_faroc.pack(side="left", padx=10, pady=10)


    # Pack the frames vertically
    frame_logs.pack(anchor="w", fill="x", pady=10, padx=20)
    
    frame_read_logiX.pack(anchor="w", fill="x", pady=10, padx=20)
    frame_write_logiX.pack(anchor="w", fill="x", pady=10, padx=20)
    
    frame_read_faroc.pack(anchor="w", fill="x", pady=10, padx=20)
    frame_write_faroc.pack(anchor="w", fill="x", pady=10, padx=20)


    # Run the main loop
    app.mainloop()


def main() -> None:
    configure_logging()
    setup_app()


if __name__ == "__main__":
    main()
    
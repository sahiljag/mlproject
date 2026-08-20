import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}.log"
log_path = os.path.join(os.getcwd(),'logs',LOG_FILE)
os.makedirs(log_path,exist_ok = True)


LOG_FILE_PATH  = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s ] %(lineno)d %(name)a %(levelname)s %(message)s",
    filename=LOG_FILE_PATH,
    filemode='w'
)
print(LOG_FILE)
print(log_path)
print(LOG_FILE_PATH)

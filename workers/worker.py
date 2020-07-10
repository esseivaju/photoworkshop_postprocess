import threading
from queue import Queue, Empty
from pyzbar.pyzbar import decode
from PIL import Image
import pytesseract
import shutil
import os
import logging


class WorkerTask():

    def __init__(self, source_img: str):
        self.img = source_img


class Worker(threading.Thread):

    def __init__(self, work_queue: Queue,  stop_event: threading.Event, move_file: bool,  project: str, name: str, dst_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setName(name)
        self.__work_queue = work_queue
        self.__stop_event = stop_event
        self.__dst = dst_dir
        self.__project = project
        self.__move_op = shutil.move if move_file else shutil.copy
        self.__logger = logging.getLogger(self.getName())

    def __find_name_in_img(self, imgpath: str):
        decoded = decode(Image.open(imgpath))
        for barcode in decoded:
            code_data = barcode.data.decode()
            if code_data.startswith(self.__project):
                if not code_data.endswith(".tif"):
                    code_data = f"{code_data}.tif"
                return code_data
        text = pytesseract.image_to_string(imgpath).splitlines()
        for line in text:
            if line.startswith(self.__project):
                return line

    def run(self):
        while not self.__stop_event.is_set():
            try:
                message = self.__work_queue.get(timeout=0.1)
            except Empty:
                continue
            else:
                img_name = self.__find_name_in_img(message.img)
                if img_name:
                    dst_file = os.path.join(self.__dst, img_name)
                    if not os.path.isfile(dst_file):
                        self.__move_op(message.img, dst_file)
                else:
                    self.__logger.warning(f"Couldnt find filename in {message.img}")
                self.__work_queue.task_done()

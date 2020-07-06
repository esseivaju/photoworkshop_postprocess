import threading
from queue import Queue, Empty
import pytesseract
import shutil
import os


class WorkerTask():

    def __init__(self, source_img: str):
        self.img = source_img


class Worker(threading.Thread):

    def __init__(self, work_queue: Queue,  stop_event: threading.Event, move_file: bool,  name: str, dst_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setName(name)
        self.__work_queue = work_queue
        self.__stop_event = stop_event
        self.__dst = dst_dir
        self.__move_op = shutil.move if move_file else shutil.copy

    def __find_name_in_img(self, imgpath: str):
        text = pytesseract.image_to_string(imgpath).splitlines()
        for line in text:
            ext = line.rsplit(".", 1)[-1]
            if ext.isalnum() and imgpath.endswith(ext):
                return ext

    def run(self):
        while not self.__stop_event.is_set():
            try:
                message = self.__work_queue.get(timeout=0.1)
            except Empty:
                continue
            else:
                img_name = self.__find_name_in_img(message.img)
                if img_name:
                    self.__move_op(message.img, os.path.join(self.__dst, img_name))
                self.__work_queue.task_done()

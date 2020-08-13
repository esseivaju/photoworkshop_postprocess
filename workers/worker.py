import threading
from queue import Queue, Empty
from pyzbar.pyzbar import decode
from PIL import Image
import pytesseract
import shutil
import os
import pathlib
import logging


class WorkerTask():

    def __init__(self, source_img: str):
        self.img = source_img


class Worker(threading.Thread):

    def __init__(self, src_dir: str, work_queue: Queue,  stop_event: threading.Event, move_file: bool,  project: str, name: str, dst_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setName(name)
        self.__work_queue = work_queue
        self.__stop_event = stop_event
        self.__dst = dst_dir
        self.__src = src_dir
        self.__project = project
        self.__move_op = shutil.move if move_file else shutil.copy
        self.__logger = logging.getLogger(self.getName())

    def __find_name_in_img(self, imgpath: str):
        decoded = decode(Image.open(imgpath))
        for barcode in decoded:
            code_data = barcode.data.decode()
            if code_data.startswith(self.__project):
                return code_data

        text = pytesseract.image_to_string(imgpath).splitlines()
        for line in text:
            if line.startswith(self.__project):
                return line

    def __extract_num_seq(self, src):
        numseq = ""
        for char in src:
            if char.isdigit():
                numseq = f"{numseq}{char}"
        return numseq

    def __rename_files_in(self, root_dir, num_seq, img_name):
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.find(num_seq) > -1:
                    relpath = os.path.relpath(dirpath, root_dir)
                    relpath = os.path.join(os.path.basename(root_dir), relpath)
                    updated_name = filename.replace(num_seq, img_name)
                    dst_path = os.path.join(self.__dst, relpath)
                    pathlib.Path(dst_path).mkdir(parents=True, exist_ok=True)
                    self.__move_op(os.path.join(root_dir, dirpath, filename), os.path.join(dst_path, updated_name))

    def __rename_files(self, original_name, basedir, img_name):
        numseq = self.__extract_num_seq(original_name)
        while basedir:
            files = os.listdir(basedir)
            for f in files:
                abs_f = os.path.join(basedir, f)
                if os.path.isdir(abs_f) and f in ["Capture"]:
                    self.__rename_files_in(abs_f, numseq, img_name)
                    return
            basedir = os.path.dirname(basedir)

    def run(self):
        while not self.__stop_event.is_set():
            try:
                message = self.__work_queue.get(timeout=0.1)
            except Empty:
                continue
            else:
                img_name = self.__find_name_in_img(message.img)
                if img_name:
                    filename = img_name if img_name.endswith(".tif") else f"{img_name}.tif"
                    relpath = os.path.relpath(os.path.dirname(message.img), self.__src)
                    dst_dir = os.path.join(self.__dst, relpath)
                    pathlib.Path(dst_dir).mkdir(parents=True, exist_ok=True)
                    dst_file = os.path.join(dst_dir, filename)
                    if not os.path.isfile(dst_file):
                        self.__move_op(message.img, dst_file)
                    original_name = os.path.basename(message.img)
                    self.__rename_files(original_name, os.path.dirname(message.img), img_name)
                else:
                    self.__logger.warning(f"Couldnt find filename in {message.img}")
                self.__work_queue.task_done()

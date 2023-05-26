import time
import threading
import logging
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from uuid import uuid4

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()

class FileMonitorService:
    def __init__(self, idle_time, check_interval):
        self.idle_time = idle_time
        self.check_interval = check_interval
        self.file_paths = {}
        self.event_handler = LogFileHandler(self)
        self.observer = Observer()
        self.observer.start()

        thread = threading.Thread(target=self.check_files)
        thread.start()

    def add_file(self, file_path):
        if file_path not in self.file_paths:
            self.file_paths[file_path] = time.time()
            self.observer.schedule(self.event_handler, path=file_path, recursive=False)
            logging.info(f'Added file {file_path} to watch list')
            return True
        else:
            return False

    def remove_file(self, file_path):
        if file_path in self.file_paths:
            del self.file_paths[file_path]
            for watch in list(self.observer._watches):
                if watch.path == file_path:
                    self.observer.unschedule(watch)
            logging.info(f'Removed file {file_path} from watch list')


    def on_modified(self, event):
        logging.info(f'File {event.src_path} has been modified')
        self.file_paths[event.src_path] = time.time()

    def check_files(self):
        while True:
            now = time.time()
            for path, last_time in self.file_paths.items():
                if now - last_time > self.idle_time:
                    logging.info(f'File {path} has not been modified for more than {self.idle_time} seconds')
            time.sleep(self.check_interval)

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, file_monitor):
        self.file_monitor = file_monitor

    def on_modified(self, event):
        self.file_monitor.on_modified(event)

class FilePath(BaseModel):
    filepath: str

service = FileMonitorService(10, 5)
watch_ids = {}

@app.post("/add")
def add_file(file: FilePath):
    file_path = file.filepath
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=401, detail="File does not exist.")

    if not service.add_file(file_path):
        raise HTTPException(status_code=400, detail="File already in watch list")
    
    watch_id = str(uuid4())
    watch_ids[watch_id] = file_path
    return {"watch_id" : watch_id}

@app.get("/remove/{watch_id}")
def remove_file(watch_id: str):
    if watch_id not in watch_ids:
        raise HTTPException(status_code=404, detail="Watch ID not found")
    
    file_path = watch_ids[watch_id]
    service.remove_file(file_path)
    del watch_ids[watch_id]
    return {"message": f"Removed {file_path} from watch list"}

@app.get("/list")
def list_files():
    return watch_ids

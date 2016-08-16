import logging
import os
import sys
import time

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class FileWatcher(LoggingEventHandler):

    def __init__(self, dir_path):

        dir_path = dir_path.replace('$HOME', os.environ['HOME'])
        self.file_name = None
        self.full_path = None
        self.file_mode = False

        self.path = dir_path

        if os.path.isfile(dir_path):
            self.file_mode = True
            self.file_name = os.path.basename(dir_path)
            self.full_path = dir_path

            self.path = os.path.dirname(dir_path)

        logging.info("Create watcher for {0}".format(self.path))

    def dispatch(self, event):
        updated_file = getattr(event, 'dest_path', event.src_path)

        if self.file_mode and self.full_path != updated_file:
            return

        super(FileWatcher, self).dispatch(event)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileWatcher(path)

    observer = Observer()
    observer.schedule(event_handler, event_handler.path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

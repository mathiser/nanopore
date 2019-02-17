import os
from datetime import datetime
from threading import Thread
from time import sleep

from backend.file_types import Fast5
from database.db import DB


class DirWatch():
    def __init__(self, fast5_path):
        self.fast5_path = fast5_path
        self.db = DB()
        self.running = True
        self.t1 = Thread(target=self.fast5_loop)
        self.t1.start()


    def fast5_loop(self):
        while self.running:
            for fol, subs, files in os.walk(self.fast5_path):
                for file in files:
                    if not file.endswith(".fast5"): continue
                    if self.db.get_fast5(file) == None:
                        self.db.insert_fast5(Fast5(filename=file, filepath=os.path.join(fol, file)))
                        print("%s; Added %s to DB" %(str(datetime.now()), file))

            sleep(60)

    def close(self):
        self.running = False
        self.t1.join()
import os
import shutil
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
            fast5s = []
            for fol, subs, files in os.walk(self.fast5_path):
                if "added" in fol: continue

                for file in files:
                    if not file.endswith(".fast5"): continue
                    if self.db.fast5_exists(file) == 0:
                        shutil.move(file, os.path.join("added", file))
                        fast5s.append(Fast5(filename=file, filepath=os.path.join(fol, "added",  file)))
                        print("%s; Added %s to DB" %(str(datetime.now()), file))

            self.db.insert_fast5s(fast5s)
            sleep(60)

    def close(self):
        self.running = False
        self.t1.join()
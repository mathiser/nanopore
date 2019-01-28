import os

class Pipeman:


    def __init__(self, path):
        basepath = path



    def checkInputPath(self):
        for fol, subs, files in os.walk(self.path):
            for file in files:
                if ".fast5" in file and not fileExists(file)

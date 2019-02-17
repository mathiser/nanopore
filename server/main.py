import argparse
import os

from backend.dir_watch import DirWatch

class Main:

    def __init__(self, fast5_path, out_path):
        self.fast5_path = fast5_path
        self.out_path = out_path

        dw = DirWatch(fast5_path=self.fast5_path)

        while True:
            command = input()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fast5dir', '-f5', type=str, default='.', help='')
    parser.add_argument('--output', '-o', type=str, default='.', help='')
    args = parser.parse_args()
    Main(args.fast5dir, args.output)
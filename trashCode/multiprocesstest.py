import multiprocessing
from multiprocessing import Process
import os
path = '/Users/stanislasgirard/Documents/Dev/GetCertificates/certexample/'
from multiprocessing import Pool

import time




def work_log(files):
    print(" File: {}".format(files))
   


def pool_handler(files):
    p = Pool()
    p.map(work_log, files)


if __name__ == '__main__':
    files = os.listdir(path)
    pool_handler(files)
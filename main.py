import csv
import time
import ssl
import socket
from multiprocessing import Process, Queue
from time import sleep

filename = "top10milliondomains.csv"
def getCertificate(hostname):
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
    s.connect((hostname, 443))
    cert = s.getpeercert()

    subject = dict(x[0] for x in cert['subject'])
    issued_to = subject['commonName']
    issuer = dict(x[0] for x in cert['issuer'])
    issued_by = issuer['commonName']
    print(issued_to)


def fileReader():
    queue = Queue()
    with open(filename, "r", newline="") as f:  # on Python 3.x use: open(filename, "r", newline="")
        reader = csv.reader(f)  # create a CSV reader
        header = next(reader)  # grab the first line and keep it as a header reference
        print("CSV header: {}".format(header))
        for row in reader:  # iterate over the available rows
            getCertificate(row[1])
        # file exhausted, entering a 'waiting for new data' state where we manually read new lines
    
fileReader()
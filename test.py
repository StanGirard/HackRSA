from multiprocessing.pool import ThreadPool as Pool
from random import randint
from time import sleep
import ssl
import socket
import csv
import time

ctx = ssl.create_default_context()
import requests

HTTPResponse = requests.packages.urllib3.response.HTTPResponse
orig_HTTPResponse__init__ = HTTPResponse.__init__
def new_HTTPResponse__init__(self, *args, **kwargs):
    orig_HTTPResponse__init__(self, *args, **kwargs)
    try:
        self.peer_certificate = self._connection.peer_certificate
    except AttributeError:
        pass
HTTPResponse.__init__ = new_HTTPResponse__init__

HTTPAdapter = requests.adapters.HTTPAdapter
orig_HTTPAdapter_build_response = HTTPAdapter.build_response
def new_HTTPAdapter_build_response(self, request, resp):
    response = orig_HTTPAdapter_build_response(self, request, resp)
    try:
        response.peer_certificate = resp.peer_certificate
    except AttributeError:
        pass
    return response
HTTPAdapter.build_response = new_HTTPAdapter_build_response

HTTPSConnection = requests.packages.urllib3.connection.HTTPSConnection
orig_HTTPSConnection_connect = HTTPSConnection.connect
def new_HTTPSConnection_connect(self):
    orig_HTTPSConnection_connect(self)
    try:
        self.peer_certificate = self.sock.connection.get_peer_certificate()
    except AttributeError:
        pass
HTTPSConnection.connect = new_HTTPSConnection_connect





def getCertificate(hostname):
    
    s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
    s.connect((hostname, 443))
    cert = s.getpeercert()

    subject = dict(x[0] for x in cert['subject'])
    issued_to = subject['commonName']
    issuer = dict(x[0] for x in cert['issuer'])
    issued_by = issuer['commonName']
    print(issued_to)

def getCertificate2(hostname):
    try:
        ssl.get_server_certificate((hostname, 443))
    except (error, timeout) as err:
        print ("No connection: {0}".format(err))

def getCertificate3(hostname):
    try:
        r = requests.get('https://' + hostname, timeout=1)
        print('Expires on: {}'.format(r))
    except(error,timeout) as err:
        print("error")


def process_line(l):
    getCertificate3(l)


def get_next_line():
    with open('top10milliondomains.csv', "r", newline="") as f:  # on Python 3.x use: open(filename, "r", newline="")
        reader = csv.reader(f)  # create a CSV reader
        header = next(reader)  # grab the first line and keep it as a header reference
        for row in reader:  # iterate over the available rows
            yield row[1]

f = get_next_line()

t = Pool()

for i in f:
    t.map(process_line, (i,))

t.join()
t.close()
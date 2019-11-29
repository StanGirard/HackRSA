import os
path = '/root/cert/'
#path = '/Users/stanislasgirard/Documents/Dev/GetCertificates/certexample/'
import mysql.connector
from functools import partial
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric import rsa
from multiprocessing import Process, freeze_support, set_start_method, Pool
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import connect

pool = None
number = 0

dbconfig = {
  'user':'admin',
  'password':'Stanley78!',
  'auth_plugin':'mysql_native_password',
  'host':'localhost',
  'database':'Certificates'
}

def init():
    global pool
    print("PID %d: initializing pool..." % os.getpid())
    pool = MySQLConnectionPool(pool_name = "mypool", pool_size = 20, **dbconfig)


def run_files(filename):
  with open(path + filename, 'rb') as content_file:
    try: 
      content = content_file.read()
      cert = x509.load_pem_x509_certificate(content, default_backend())
      issuer = 'undefined'
      subjectCN = 'undefined'
      subjectON = 'undefined'
      publicKey = 'not RSA'
      publicKeye = "0"
      publicKeyn = "0"
      keySize = "0"
      # Get Issuer
      if cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME):
          issuer = cert.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
      
      #Get Subject Common Name
      if cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME):
          subjectCN = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
      

      #Get Key Size
      if cert.public_key:
          keySize = cert.public_key().key_size

      if isinstance(cert.public_key(), rsa.RSAPublicKey):
          publicKey = cert.public_key().public_numbers()
          publicKeye = publicKey.e
          publicKeyn = publicKey.n


      sql = "INSERT INTO Certificates.certificates (filename, issuerON, subjectCN, pubkeye, pubkeyn, keysize)  VALUES (%s, %s, %s, %s, %s, %s);" 
      con = pool.get_connection()
      c = con.cursor()
      result = c.execute(sql, (filename, issuer, subjectCN, str(publicKeye), str(publicKeyn), str(keySize)))
      global number
      number += 1
      con.close()
      
      if number % 100 == 0:
        print(number)
    except mysql.connector.Error as err:
      print(err)
    except:
      print("Error")
    

  
  

if __name__ == '__main__':
  set_start_method('spawn')
  freeze_support()
  number = 0
  p = Pool(initializer=init)
  print("Db connection")
  try:
      
      files = os.listdir(path)
      p.map(run_files,  files)
      p.close()
      p.join()  
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  






import os
path = '/root/SSLCert/cert/'
#path = '/Users/stanislasgirard/Documents/Dev/GetCertificates/certexample/'
import mysql.connector
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric import rsa

from mysql.connector import errorcode
number = 0
try:
    cnx = mysql.connector.connect(user='admin', password='Stanley78!',
                              host='localhost',
                              database='Certificates')
    cursor = cnx.cursor()
    for filename in os.listdir(path):
        
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


            sql = "INSERT INTO Certificates.decoded (filename, issuerON, subjectCN, pubkeye, pubkeyn)  VALUES (%s, %s, %s, %s, %s);" 
            
            print(publicKeyn)
            result = cursor.execute(sql, (filename, issuer, subjectCN, publicKeye, publicKeyn))
            cnx.commit()
            number += 1
            if number % 100 == 0:
              print(number)
          except mysql.connector.Error as err:
            print(err)
          except:
            print("Error") 
            
            
            
            
            
        
    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)






import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID, ExtensionOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives.asymmetric import rsa

def get_certs(domain):
    content = ssl.get_server_certificate((domain, 443))
    cert = x509.load_pem_x509_certificate(content.encode('utf-8'), default_backend())
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
    return [issuer, subjectCN, subjectON, publicKeye, publicKeyn, keySize]

print(get_certs("epita.fr"))
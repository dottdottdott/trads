import pgpy
from solidsocial.models import Author
from dssd.settings import PGP_PKEY

def check_signed(content):
    try:
        msg = pgpy.PGPMessage.from_blob(content)
        return True
    except:
        return False

def check_signature(content, wid):
    msg = pgpy.PGPMessage.from_blob(content)
    if author:=Author.objects.filter(url=wid):
        if key:=author.first().key:
            key = key.encode().decode('unicode_escape')[2:-1]
            key = f"{key[-1]}{key[:-1]}"
            pgp_pub = pgpy.PGPKey()
            pgp_pub.parse(key)
            valid = bool(pgp_pub.verify(msg))
            return valid, msg.message
    return False, msg.message
 
def sign_message(message):
    ''' Sign message using private pgp key stored in django settings '''
    pgp_pkey = pgpy.PGPKey()
    pgp_pkey.parse(PGP_PKEY)
    return str(pgp_pkey.sign(message))

def verify_signature(message, signature, key):
    ''' Check signature of a message using provided pubkey '''
    pgp_pub = pgpy.PGPKey()
    pgp_pub.parse(key)
    pgp_sig = pgpy.PGPSignature()
    pgp_sig.parse(signature)
    if pgp_pub.verify(message[:-1], pgp_sig):
        return True
    else:
        return False

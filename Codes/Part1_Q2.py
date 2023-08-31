import ecdsa
import hashlib
import base58

def generatePrivateKey():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    return private_key

def generatePublicKey(private_key):
    public_key = private_key.get_verifying_key()
    return public_key

def wif(private_key):
    TestnetPrivateKey = b'\xEF'
    key =  TestnetPrivateKey + private_key

    sha1 = hashlib.sha256(key)
    sha1 = sha1.digest()

    sha2 = hashlib.sha256(sha1)
    sha2 = sha2.digest()

    checksum_bytes = sha2[:4]
    result = key + checksum_bytes
    result = base58.b58encode(result)
    return result

def p2pkh(public_key):
    sha256 = hashlib.sha256(public_key)
    sha256 = sha256.digest()
    hash_160 = hashlib.new('ripemd160')
    hash_160.update(sha256)
    hash_160 = hash_160.digest()
    hash_160 = b'\x6F' + hash_160

    sha1 = hashlib.sha256()
    sha1.update(hash_160)
    sha1 = sha1.digest()

    sha2 = hashlib.sha256()
    sha2.update(sha1)
    sha2 = sha2.digest()

    checksum_bytes = sha2[:4]
    result = hash_160 + checksum_bytes
    result = base58.b58encode(result)
    return result

def vanity(goal):
    while True:
        private_key = generatePrivateKey()
        public_key = b'\x04' + generatePublicKey(private_key).to_string()
        address = p2pkh(public_key)
        if goal == address[1:4]:
            return address, private_key, public_key

vanity_address, private_key, public_key = vanity(b'san')
print("Private Key : " + private_key.to_string().hex())
print("Public Key : " + public_key.hex())
print("Private WIF : " + wif(private_key.to_string()).decode('utf-8'))
print("Vanity Address : " + vanity_address.decode('utf-8'))
import bitcoin.wallet
import struct, time
from bitcoin.core import b2lx, b2x
from utils import *
from hashlib import sha256

MAGIC_NUMBER = 0xD9B4BEF9
bitcoin.SelectParams("mainnet")
my_private_key = bitcoin.wallet.CBitcoinSecret('5J1LiPRjoLbvB6eAtETsDnfBQLDGTmVzvDBESc7bG51ZUy23jQ3')
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key), OP_EQUALVERIFY, OP_CHECKSIG]

def make_transaction(txid, utxo_index, block_reward, data):
    txout_scriptPubKey = P2PKH_scriptPubKey()

    txin = create_txin(txid, utxo_index)
    txout = create_txout(block_reward, txout_scriptPubKey)
    txin.scriptSig =  CScript([int(data, 16).to_bytes(len(data)//2, 'big')])

    return CMutableTransaction([txin], [txout])

def target(bits):
    coefficient = bits[4:]
    exponent = bits[2:4]

    target = int(coefficient, 16) * (int('2', 16) ** (8 * (int(exponent, 16) - 3)))
    target_hex = str(format(target, 'x')).zfill(64)
    print("target: ", target_hex,"\n")
    return bytes.fromhex(target_hex)

def get_block():
    block_size = len(b'\x01') + len(header) + len(block_body)
    block = MAGIC_NUMBER.to_bytes(4, "little") + struct.pack("<L", block_size) + header + b'\x01' + block_body
    print(b2x(block))

if __name__ == '__main__':
    prev_hash_blocks = '00000000b34ff50a225ae6d5a127ae5a8ad8f3c96a0a3a3bdb41976b8a2eb450'

    version = 2
    block_reward = 6.25
    data = '810199435SanaSariNavaei'.encode('utf-8').hex()
    txid = (64*'0')
    utxo_index = int('0xFFFFFFFF', 16)
    bits = '0x1f010000'

    tx = make_transaction(txid, utxo_index, block_reward, data)
    block_body = b2x(tx.serialize())
    merkle_root = b2lx(sha256(sha256(tx.serialize()).digest()).digest())
    print("block body: ", block_body,"\n")
    print("merkle root: ", merkle_root,"\n")

    target = target(bits)
    get_time = int(time.time())
    partial_header = struct.pack("<L", version) + bytes.fromhex(prev_hash_blocks)[::-1] + bytes.fromhex(merkle_root)[::-1] + struct.pack('<LL', get_time, int(bits, 16))

    nonce = 0
    time_now = time.time()
    max_num =  0xFFFFFFFF
    while nonce <= max_num:
        header = partial_header + struct.pack('<L', nonce)
        block_hash = sha256(sha256(header).digest()).digest()
        if block_hash[::-1] < target:
            
            print ("nonce: ", nonce)
            print("Hash rate: ", nonce / (time.time() - time_now))
            print("Header: ", header)
            print("Block Hash: ", block_hash)
            print("Block Body: ", block_body)
            break

        nonce += 1

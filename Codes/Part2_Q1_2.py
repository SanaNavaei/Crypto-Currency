import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret('92pQfWUUM6zHkwiZSzK2QENzNswnH7BYtctSGkeTwN7ef79ETNC') # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def send_P2PKH_tx(amount_to_spend, txid_to_spend, utxo_index, txout_scriptPubKey):
    txin = create_txin(txid_to_spend, utxo_index)
    txout = create_txout(amount_to_spend, txout_scriptPubKey)

    txin_scriptPubKey = [OP_1]
    txin_scriptSig = []
    tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(tx)

if __name__ == '__main__':
    amount_to_spend = 0.01675
    txid_to_spend = ('992bbf6f8082685f5c543abe4ca42eb6e22a893fc9b79270ec0185d4c95ea1a1')
    utxo_index = 0

    print("my_address: ", my_address)
    print("my_public_key: ", my_public_key.hex())
    print("my_private_key: ", my_private_key.hex())

    txout_scriptPubKey = P2PKH_scriptPubKey()
    response = send_P2PKH_tx(amount_to_spend, txid_to_spend, utxo_index, txout_scriptPubKey)

    print("response status code: " ,response.status_code, "response reason: ", response.reason)
    print("response text: ", response.text)
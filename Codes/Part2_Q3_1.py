import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("92pQfWUUM6zHkwiZSzK2QENzNswnH7BYtctSGkeTwN7ef79ETNC") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
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

    txin_scriptPubKey = P2PKH_scriptPubKey()
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(tx)

if __name__ == '__main__':
    prime_1 = 4639
    prime_2 = 6269
    Sum = prime_1 + prime_2  #10908
    Sub = prime_2 - prime_1  #1630

    amount_to_spend = 0.0147
    txid_to_spend = ('b72401a24a1814f85eb836dbb1b271d643e79241e7b52996271c567f6cc8ac7b')
    utxo_index = 0

    txout_scriptPubKey = [OP_2DUP, OP_SUB, OP_HASH160, Hash160((Sub).to_bytes(2, byteorder="little")), OP_EQUALVERIFY, OP_ADD,
                          OP_HASH160, Hash160((Sum).to_bytes(2, byteorder="little")), OP_EQUAL]
    response = send_P2PKH_tx(amount_to_spend, txid_to_spend, utxo_index, txout_scriptPubKey)

    print("response status code: " ,response.status_code, "response reason: ", response.reason)
    print("response text: ", response.text)

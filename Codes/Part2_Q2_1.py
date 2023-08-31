import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("92pQfWUUM6zHkwiZSzK2QENzNswnH7BYtctSGkeTwN7ef79ETNC") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

private_key1= bitcoin.wallet.CBitcoinSecret('922NDRTK861R1aAmbJ9PWFy53EFRXYQmEodoCRmngUgf5uAvtua')
public_key1 = private_key1.pub

private_key2 = bitcoin.wallet.CBitcoinSecret('91jxGSKPdLsqnpDR1cdkC2Qg1xi6TuiUxxS5KYax5BUqhezx68B')
public_key2 = private_key2.pub

private_key3 = bitcoin.wallet.CBitcoinSecret('92WRR9mH2pbvVkHHPhjcLcGBhXKvdSQEE3spUsTBvG621T42khZ')
public_key3 = private_key3.pub

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
    amount_to_spend = 0.01635
    txid_to_spend = ('cc0fdb6bc13d0dc67db2936a1f138343fc110db4361b938e2f9b57ef00821aba')
    utxo_index = 0

    print("my_address: ", my_address)
    print("my_public_key: ", my_public_key.hex())
    print("my_private_key: ", my_private_key.hex())

    txout_scriptPubKey = [OP_2, public_key1, public_key2, public_key3, OP_3, OP_CHECKMULTISIG]
    response = send_P2PKH_tx(amount_to_spend, txid_to_spend, utxo_index, txout_scriptPubKey)

    print("response status code: " ,response.status_code, "response reason: ", response.reason)
    print("response text: ", response.text)
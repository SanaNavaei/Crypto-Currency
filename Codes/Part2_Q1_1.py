import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret('92pQfWUUM6zHkwiZSzK2QENzNswnH7BYtctSGkeTwN7ef79ETNC')
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

def P2PKH_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout_1, txout_2, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature2(txin, txout_1, txout_2, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def send_P2PKH_tx_two_outputs(amount_to_send1, amount_to_send2, txid_to_spend, utxo_index):
    txin = create_txin(txid_to_spend, utxo_index)
    txout_1 = create_txout(amount_to_send1, [OP_1])
    txout_2 = create_txout(amount_to_send2, [OP_0])

    txin_scriptPubKey = P2PKH_scriptPubKey()
    txin_scriptSig = P2PKH_scriptSig(txin, txout_1, txout_2, txin_scriptPubKey)
    tx = create_signed_transaction2(txin, txout_1, txout_2, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(tx)

if __name__ == '__main__':
    amount_to_spend_1 = 0.01677
    amount_to_spend_2 = 0.000001
    txid_to_spend = ('f3545397ffb3e150b7fbb8d0cbff55aaf265a5eb772cc8969a590f6a1bab1c2d')
    utxo_index = 1

    print("my_address: ", my_address)
    print("my_public_key: ", my_public_key.hex())
    print("my_private_key: ", my_private_key.hex())

    response = send_P2PKH_tx_two_outputs(amount_to_spend_1, amount_to_spend_2, txid_to_spend, utxo_index)

    print("response status code: " ,response.status_code, "response reason: ", response.reason)
    print("response text: ", response.text)
    
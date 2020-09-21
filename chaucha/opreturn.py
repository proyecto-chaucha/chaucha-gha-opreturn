from . import crypto
from . import insight
from . import constants

from binascii import a2b_hex, b2a_hex
from bitcoin import mktx, mksend, sign

# Decoding an OP_RETURN
# use xxd -p -r in a terminal
# e.g.
# echo 486f6c61204d756e646f | xxd -p -r

# Max number of chars in OP_RETURN
MAX = 255


def __payload(string):
    metadata = bytes(string, "utf-8")
    metadata_len = len(metadata)

    if metadata_len <= 75:
        payload = bytearray((metadata_len,)) + metadata
    elif metadata_len <= 256:
        payload = b"\x4c" + bytearray((metadata_len,)) + metadata
    else:
        payload = (
            b"\x4d"
            + bytearray((metadata_len % 256,))
            + bytearray((int(metadata_len / 256),))
            + metadata
        )

    return payload


def send(privkey, pubkey, sendto, message="", force=False):

    op_return = message

    addr = pubkey

    confirmed_balance, inputs, unconfirmed = insight.getunspentbalance(addr)

    if not force:
        if not crypto.pubkey_is_valid(addr):
            # Invalid Address
            # print("Invalid Address")
            return False

        elif constants.FEE_MINIMUM > confirmed_balance:
            # Not enough chauchas
            # print("No minimum fee")
            return False

        elif len(op_return) > MAX:
            # Message too long
            # print("Message to long")
            return False

    # Transformar valores a Chatoshis
    used_amount = int(constants.FEE_MINIMUM * constants.COIN)

    # Utilizar solo las unspent que se necesiten
    used_balance = 0
    used_inputs = []

    for i in inputs:
        used_balance += i["value"]
        used_inputs.append(i)
        if used_balance > used_amount:
            break

    # Output
    outputs = [{"address": sendto, "value": used_amount}]

    # OP_RETURN
    if len(op_return) > 0 and len(op_return) <= MAX:
        payload = __payload(op_return)
        script = constants.OP_RETURN + b2a_hex(payload).decode("utf-8", errors="ignore")

        outputs.append({"value": 0, "script": script})

    # Transaction
    template_tx = mktx(used_inputs, outputs)
    size = len(a2b_hex(template_tx))

    # FEE = 0.01 CHA/kb
    # MAX FEE = 0.1 CHA

    fee = int((size / constants.KYLOBYTE) * constants.FEE_RECOMMENDED * constants.COIN)
    fee = constants.FEE_MAX if fee > constants.FEE_MAX else fee

    if used_balance == confirmed_balance:
        outputs[0] = {"address": sendto, "value": used_amount - fee}
        tx = mktx(used_inputs, outputs)
    else:
        tx = mksend(used_inputs, outputs, addr, fee)

    for i in range(len(used_inputs)):
        tx = sign(tx, i, privkey)

    broadcasting = insight.broadcast(tx)

    try:
        msg = insight.endpoint() + "/tx/%s" % broadcasting.json()["txid"]
    except Exception:
        msg = broadcasting.text

    return msg

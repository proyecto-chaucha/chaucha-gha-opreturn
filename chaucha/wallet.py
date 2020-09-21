"""
Wallet related functions
"""
from . import crypto
from . import constants


def new(string=crypto.uid()):

    if not string or str(string).strip() == "":
        string = crypto.uid()

    privkey = crypto.new("sha256", str(string).encode()).hexdigest()

    b58_PUBKEY_ADDRESS = str(constants.CHAUCHA_PUBKEY_ADDRESS)
    b58_SECRET_KEY = str(constants.CHAUCHA_SECRETKEY)

    checksum = crypto.doubleSHA256(b58_SECRET_KEY + privkey)[:8]
    wif = crypto.b58check(crypto.a2b_hex(b58_SECRET_KEY + privkey + checksum))

    pubkey = crypto.secp256k1(privkey)
    pubkeyhash = crypto.hash160(pubkey)

    checksum = crypto.doubleSHA256(b58_PUBKEY_ADDRESS + pubkeyhash)[:8]
    addr = crypto.b58check(crypto.a2b_hex(b58_PUBKEY_ADDRESS + pubkeyhash + checksum))

    return (wif.decode("utf-8"), addr.decode("utf-8"))


def is_valid(pubkey):
    return crypto.check_address(str(pubkey))

# General
KYLOBYTE = 1024
DIGITS58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# Chaucha
INSIGHT_ENDPOINT = "https://explorer.cha.terahash.cl"

CHAUCHA_PUBKEY_ADDRESS = 58
CHAUCHA_SECRETKEY = "d8"

# Minimum unit 10^-8 CHA
# Included other alternate versions
CHATOSHI = 100_000_000
SATOSHI = CHATOSHI
COIN = CHATOSHI

# Used in Address generation
# The 'c' char must be first
CBYTE = 88
MAGIC = CBYTE

# Transaction fees
FEE_RECOMMENDED = 0.01
FEE_MINIMUM = 0.001
FEE_BASE = 0.000452
FEE_PER_INPUT = 0.000296
FEE_MAX = 10_000_000

# Operator Codes
OP_RETURN = "6a"
OP_CHECKLOCKTIMEVERIFY = "b1"
OP_DROP = "75"
OP_CHECKSIG = "ac"
OP_HASH160 = "a9"
OP_EQUAL = "87"
OP_HASH256 = "aa"
OP_PUSHDATA1 = "0a"

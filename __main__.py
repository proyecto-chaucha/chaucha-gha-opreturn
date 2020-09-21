import gha
from sys import exit
from os import getenv
from chaucha import opreturn


def main():

    privkey = getenv("INPUT_PRIVKEY")

    if not privkey:
        gha.error("Private Key not found")
        exit(-1)

    pubkey = getenv("INPUT_PUBKEY")

    if not pubkey:
        gha.error("Public Key not found")
        exit(-1)

    sendkey = getenv("INPUT_SENDKEY")

    if not sendkey:
        gha.error("Send Key not found")
        exit(-1)

    message = getenv("INPUT_MESSAGE")

    if not message:
        gha.error("Message not found")
        exit(-1)

    gha.debug("Sending the OP_RETURN")
    response = opreturn.send(privkey, pubkey, sendkey, message)

    if not response:
        gha.error("Could not send OP_RETURN")
        exit(-1)

    gha.debug(response)
    gha.output("response", response)
    exit(0)


if __name__ == "__main__":
    main()

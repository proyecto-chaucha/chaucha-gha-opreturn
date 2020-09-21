import action
from sys import exit
from os import getenv
from chaucha import opreturn


def main():

    privkey = getenv("INPUT_PRIVKEY")

    if not privkey:
        action.error("Private Key not found")
        exit(-1)

    pubkey = getenv("INPUT_PUBKEY")

    if not pubkey:
        action.error("Public Key not found")
        exit(-1)

    sendkey = getenv("INPUT_SENDKEY")

    if not sendkey:
        action.error("Send Key not found")
        exit(-1)

    message = getenv("INPUT_MESSAGE")

    if not message:
        action.error("Message not found")
        exit(-1)

    action.debug("Sending the OP_RETURN")
    response = opreturn.send(privkey, pubkey, sendkey, message, force=True)

    if not response:
        action.error("Could not send OP_RETURN")
        exit(-1)

    action.debug(response)
    action.output("response", response)
    exit(0)


if __name__ == "__main__":
    main()

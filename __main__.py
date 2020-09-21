from os import getenv
from chaucha import opreturn


def main():
    privkey = getenv("INPUT_PRIVKEY")
    pubkey = getenv("INPUT_PUBKEY")
    sendkey = getenv("INPUT_SENDKEY")
    message = getenv("INPUT_MESSAGE")

    response = opreturn.send(privkey, pubkey, sendkey, message)

    print(f"::set-output name=response::{response}")


if __name__ == "__main__":
    main()

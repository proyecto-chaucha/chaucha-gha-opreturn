from requests import get, post
from binascii import a2b_hex
from .constants import INSIGHT_ENDPOINT
from os import getenv


def endpoint():
    return getenv("INSIGHT_ENDPOINT") or INSIGHT_ENDPOINT


def broadcast(tx):
    url = endpoint() + "/api/tx/send"
    broadcasting = post(url, data={"rawtx": tx})
    return broadcasting


def checklocktime(script):
    url = endpoint() + "/api/status?getInfo"
    last_block = get(url).json()["info"]["blocks"]
    locktime = getlocktime(script)

    return int(last_block) >= int(locktime)


def gethistory(addr, page=0):
    url = endpoint() + "/api/txs/?address="
    history = get(url + addr + "&pageNum=" + str(page)).json()

    txs = []
    for i in history["txs"]:
        actual = localtime(int(i["time"]))
        date = strftime("%d.%m.%Y %H:%M:%S", actual)
        msg = ""
        for j in i["vout"]:
            hex_script = j["scriptPubKey"]["hex"]
            if hex_script.startswith("6a"):
                if len(hex_script) <= 77 * 2:
                    sub_script = hex_script[4:]
                else:
                    sub_script = hex_script[6:]

                msg = a2b_hex(sub_script).decode("utf-8", errors="ignore")

        tx = {
            "confirmations": i["confirmations"],
            "txid": i["txid"],
            "time": date,
            "msg": msg,
        }

        txs.append(tx)

    return [txs, history["pagesTotal"]]


def getbalance(addr):
    url = endpoint() + "/api/addr/"
    balance = get(url + addr).json()
    return round(float(balance["balance"]), 8)


def getunspentbalance(addr):
    unspent = get(endpoint() + "/api/addr/" + addr + "/utxo").json()

    confirmed = unconfirmed = 0

    inputs = []
    for i in unspent:
        if i["confirmations"] >= 1 and i["amount"] >= 0.001:
            confirmed += i["amount"]
            inputs_tx = {
                "output": i["txid"] + ":" + str(i["vout"]),
                "value": i["satoshis"],
                "address": i["address"],
            }

            inputs.append(inputs_tx)
        else:
            unconfirmed += i["amount"]

    return [confirmed, inputs, unconfirmed]


def getunspent(addr, sendamount=0):
    # Captura de balance por tx sin gastar
    url = endpoint() + "/api/addr/"
    try:
        unspent = get(url + addr + "/utxo").json()
    except Exception:
        return False

    # Variables auxiliares
    inputs = []
    confirmed = unconfirmed = unspent_balance = 0

    for i in unspent:
        if i["confirmations"] >= 6:
            confirmed += i["amount"]

            if sendamount > 0:
                unspent_balance += i["amount"]
                inputs_tx = {
                    "output": i["txid"] + ":" + str(i["vout"]),
                    "value": i["satoshis"],
                    "address": i["address"],
                }

                inputs.append(inputs_tx)
                if unspent_balance >= int(sendamount):
                    break
        else:
            unconfirmed += i["amount"]
    if sendamount > 0:
        return {"used": round(unspent_balance, 8), "inputs": inputs}
    else:
        return [confirmed, unconfirmed]

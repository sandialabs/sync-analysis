import os
import sys
import time
import json
import logging
import requests

from numpy.random import exponential, choice, randint
from datetime import datetime, timedelta
from threading import Thread
from os import environ as env

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, "frankenstein.txt")) as fd:
    WORDS = "".join(
        x.lower() for x in fd.read() if x.isascii() and x.isalpha() or x.isspace()
    ).split()

NUM_WORDS = 8


def call(function, *arguments):
    result = requests.post(
        f"http://{env['JOURNAL']}/interface/json",
        json={
            "function": function,
            "arguments": arguments,
            "authentication": env["SECRET"],
        },
    ).json()

    logger.info(f"{datetime.now().isoformat()} {function} | {arguments} -> {result}")
    return result


def run(peers):
    # initialize peering
    for peer in peers[env["JOURNAL"]]:
        # todo: handle public key
        while r := call("peer!", peer.rsplit(".", 1)[0], {"*type/string*": f"http://{peer}/interface"}):
            if r is not True:
                logger.warning(f"Could not peer with {peer}, trying again")
                time.sleep(1)
            else:
                break

    # preload the journal
    for i in range(int(env["SIZE"])):
        call(
            "set!",
            [["*state*", "data", f"key-{i}"]],
            " ".join(choice(WORDS, NUM_WORDS)),
        )

    # perform a single action
    def _act(call):
        path, node = [], env["JOURNAL"]
        while choice(2) and peers.get(node):
            node = choice(peers[node])
            path += [-1, ["*peers*", node.rsplit(".", 1)[0], "chain"]]

        path += [-1, ["*state*", "data", f"key-{randint(0, env['SIZE'])}"]]

        # read from the journal
        result = call("get", [path])

        if type(result) is not str:
            logger.warning("Cannot complete action")
            return

        ls = result.split(" ")
        ls[randint(0, NUM_WORDS)] = choice(WORDS)

        # # write to the journal
        call(
            "set!",
            [["*state*", "data", f"key-{randint(0, env['SIZE'])}"]],
            " ".join(result),
        )

    until = datetime.now()
    while True:
        Thread(target=_act, args=[call]).start()
        time.sleep(max((until - datetime.now()).total_seconds(), 0))
        until += timedelta(seconds=int(env["ACTIVITY"]))


if __name__ == "__main__":
    # poll until journal is up
    while True:
        try:
            int(call("size"))
            break
        except Exception:
            time.sleep(1)

    with open(os.path.join(DIR, "peers.json")) as fd:
        peers = json.load(fd)

    run(peers)

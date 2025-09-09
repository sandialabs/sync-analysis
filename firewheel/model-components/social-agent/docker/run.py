import os
import sys
import time
import json
import logging
import requests

from datetime import datetime
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


def call(query):
    result = requests.post(
        f"http://{env['JOURNAL']}/.interface",
        '(*local* "{}" {})'.format(
            env["SECRET"],
            query,
        ),
    ).text

    logger.info(f"{datetime.now().isoformat()} {query} -> {result}")
    return result


def run(peers):
    # initialize peering
    for peer in peers[env["JOURNAL"]]:
        while r := call(
            '(ledger-peer! {} (lambda (msg) (sync-remote "{}" msg)))'.format(
                peer.rsplit(".", 1)[0],
                f"http://{peer}/.interface",
            )
        ):
            if r != "#t":
                logger.warning(f"Could not peer with {peer}, trying again")
                time.sleep(1)
            else:
                break

    # preload the ledger
    for i in range(int(env["SIZE"])):
        call(
            '(ledger-set! (*state* data {}) "{}"))'.format(
                f"key-{i}",
                " ".join(choice(WORDS, NUM_WORDS)),
            )
        )

    # perform a single action
    def _act(call):
        path, node = [], env["JOURNAL"]
        while choice(2) and peers.get(node):
            node = choice(peers[node])
            path += ["*peers*", node.rsplit(".", 1)[0]]

        path += ["*state*", "data", f"key-{randint(0, env['SIZE'])}"]

        # read from the ledger
        query = f"(ledger-get ({' '.join(path)}))"
        response = call(query)

        if not response.startswith("(object "):
            logger.warning("Cannot complete action")
            return

        ls = response[9:-2].split(" ")
        ls[randint(0, NUM_WORDS)] = choice(WORDS)

        # # write to the ledger
        call(
            '(ledger-set! (*state* data {}) "{}")'.format(
                f"key-{randint(0, env['SIZE'])}",
                " ".join(ls),
            )
        )

    until = datetime.now()
    while True:
        Thread(target=_act, args=[call]).start()
        time.sleep(max((until - datetime.now()).total_seconds(), 0))
        until += timedelta(
            seconds=exponential(
                2
                ** (
                    sum(
                        [
                            int(env["PERIODICITY"]),
                            -int(env["ACTIVITY"]),
                        ]
                    )
                )
            )
        )


if __name__ == "__main__":
    # poll until journal is up
    while True:
        try:
            int(call("(ledger-index)"))
            break
        except Exception:
            time.sleep(1)

    with open(os.path.join(DIR, "peers.json")) as fd:
        peers = json.load(fd)

    run(peers)

import json
import os
from itertools import count
from typing import NoReturn

import zmq
from tqdm import tqdm
from zmq import Context, Socket


def serve(socket: Socket) -> NoReturn:
    print("Publishing")
    for c in tqdm(range(1_000_000_000)):
        # msg = json.dumps(
        #     {
        #         "id": c,
        #         "key": "some value",
        #     }
        # ).encode("utf-8")
        socket.send(b'{ "id": 1, "key": "some value" }')


def main():
    port = os.environ.get("ZMQ_BIND_PORT")
    if port is None:
        raise RuntimeError("PORT environment variable not set")

    with Context() as ctx:
        sck = ctx.socket(zmq.PUB)
        with sck.bind(f"tcp://*:{port}") as sck:
            print("Bound to port", port)
            sck.set(zmq.SocketOption.SNDHWM, 1000)
            serve(sck)


if __name__ == "__main__":
    main()

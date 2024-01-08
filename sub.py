import asyncio
import json
import os
from typing import NoReturn

import zmq
from zmq.asyncio import Context, Socket


async def on_message(msg: bytes):
    print(json.loads(msg))


async def listen(socket: Socket) -> NoReturn:
    while True:
        msg = await socket.recv()
        await on_message(msg)


async def main():
    port = os.environ.get("ZMQ_BIND_PORT")
    if port is None:
        raise RuntimeError("PORT environment variable not set")

    with Context() as ctx:
        sck = ctx.socket(zmq.SUB)
        with sck.connect(f"tcp://localhost:{port}") as sck:
            sck.set(zmq.SocketOption.SUBSCRIBE, b"")
            sck.set(zmq.SocketOption.RCVHWM, 1000)
            await listen(sck)


if __name__ == "__main__":
    asyncio.run(main())

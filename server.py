import asyncio
import aioconsole
from PIL import Image
import os

async def start_server(on_client_connect,host,port):
    server = await asyncio.start_server(on_client_connect,host,port)
    await server.serve_forever()

async def main():
    await start_server(handle_handshake,'127.0.0.1',65431)

asyncio.run(main())
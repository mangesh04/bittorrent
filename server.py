import asyncio
import aioconsole
from PIL import Image
import os



async def send_hand_shake(writer):
    writer.write()
    await writer.drain()

async def send_file(writer,file,chunk_size=16*1024):

    with open(f,'rb') as f:
        chunk=f.read(chunk_size)
        while chunk:
            # print(chunk)
            writer.write(chunk)
            await writer.drain()
            chunk=f.read(chunk_size)

    writer.close()
    await writer.wait_closed()

def handles_messages(reader,writer):
    if(have_pieces):
        writer.write(bitfield)
    while True:
        message_len=reader.read(4)
        message_id=reader.read(1)

    if message_id == 


def check_handshake():
    pass
async def handle_handshake(reader, writer):
    handshake=await reader.read(100)
    check_handshake(handshake)
    handles_messages(reader,writer)

async def start_server(on_client_connect,host,port):
    server = await asyncio.start_server(on_client_connect,host,port)
    await server.serve_forever()

async def main():
    await start_server(handle_handshake,'127.0.0.1',65431)

asyncio.run(main())
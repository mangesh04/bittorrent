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

async def handle_messages(reader,writer):
    while True:
        try:
            message_length = await asynciowait_for (reader.read(4),300)
            message_lenth=struct.unpack('!I',  message_lenth)
        except asyncio.TimeoutError:
            await aioconsole.aprint("time out  connection dropped with ")
            writer.close()
            break
        if message_length == 0:
            continue
        message_id= await reader.read(1)
        if message_id==2:#intrested
            pass
        if message_id==3:#not intrested
            pass
        if message_id==4:#have
            pass
        if message_id==6:#request
            pass
        if message_id==8:#cancel
            pass



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
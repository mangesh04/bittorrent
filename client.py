import asyncio
import aioconsole
from PIL import Image
import io
import requests
import aiohttp
import json

class async_tcp_client:

    async def close_writer():
        writer.close()
        await writer.wait_closed()

    async def send_message(writer):
        message=await aioconsole.ainput()
        writer.write(message.encode())
        await writer.drain()

    async def receive_message(reader):
        data = await reader.read(100)
        return data

    async def connect_server(host,port):
        return  await asyncio.open_connection(host, port)

    async def download_file(host,port,chunk=16*1024):

        reader , writer= await connect_server(host,port)

        file = bytearray()

        while True:
            new_data=await reader.read(chunk)
            if not new_data:
                break
            peice.extend(new_data)

        return file

    async def read_print(reader):
        while(True):
            message=await receive_message(reader)
            if message:
                await aioconsole.aprint(message)


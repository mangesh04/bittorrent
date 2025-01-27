import hashlib
import requests
import random
import bencodepy
import struct
import asyncio
import aioconsole
from PIL import Image
import io
import pprint
from functools import cmp_to_key
from bitarray import bitarray
import essencial_funcs


peice_count=[-1 for i in range(bitmap_length)]
rank_count=[]
bd=bencode_decoder()
decoded_tf=bd.decode_fil(torrent_file)
peers={}
bitmap_length=9
downloaders_limit=3

def update_rank_count():
    for i in peice_count:
        rank_count[i-1]+=1

    for i in range(bitmap_length-1):
        rank_count[i+1]+=rank_count[i]

def get_next_task(peer_id):
    if rank_count[peers[peer_id]['rank']] <=downloaders_limit:
        return 1 #send request message
    else:
        return 0 #send keep alive message


def sort_peers():
    def compare(a,b):
        if a['uploaded']<b['uploaded']:
            return 1
        else:
            return -1
    peers=sorted(peers,key=cmp_to_ke(compare))

def request_message(index,begin,block):
    request=struct.pack('!IB',13,6,index,beginblock)
    return request

async def download_piece(reader,writer):
    piece=bitarray()
    request=request_message()
    await writer.write(request)
    new_data=await reader.read(chunk)
    if not new_data:
        break
    peice.extend(new_data)





async def tcp_client():

    async def connect_server(host,port):
        return  await asyncio.open_connectio(host, port)


    async def receive_packet(host,portchunk=16*1024):
        while True:
            new_data=await reader.read(chunk)
            if not new_data:
                break
            peice.extend(new_data)
        return file


    async def request_message_loop(peer_id):
        while True:
            if get_next_task(peer_id):
                #send request message
                    await receive_packet(peer)


    async def handle_messages(reader,writer):

        #handshake
        #got peer id here
        #bitfield
        #interested/not interested
        #chock/unchocked

        while True:

            try:
                message_length = await asyncio.wait_for (reader.read(4),300)
                message_lenth=struct.unpack('!I',   message_lenth)
            except asyncio.TimeoutError:
                await aioconsole.aprint("time out   connection dropped with ")
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
                await request_message_loop(peer_id)

            if message_id==8:#cancel
                pass
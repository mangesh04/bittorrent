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
from bencode_decoder import bencode_decoder

class torrent_client_side:
    bitmap=bitarray()
    peers={}
    url_para={}

    def __init__(self,torrent_file):
        self.bd=bencode_decoder()
        self.decoded_tf=self.bd.decode_file(torrent_file)
        self.set_url_parameters()
        self.update_peers()

    def create_peer_id(self,client_id):
        return f"{client_id}{''.join([str(random.randint(0,   9)) for _ in range(12)])}"

    def file_size(self):

        temp=0
        if b"files" in self.decoded_tf[b"info"]:
            sum=0
            for i in self.decoded_tf[b"info"][b"files"]:
                sum+=i[b"length"]
            temp=sum
        else:
            temp=int(str(self.decoded_tf[b"info"][b"length"]).encode(),10)

        return temp

    def set_url_parameters(self):
        self.url_para['announce'] =self.decoded_tf  [b"announce"].decode()

        self.url_para['peer_id']=self.create_peer_id('-MT0001-')

        self.info_hash=hashlib.sha1(self.bd.encode(self. decoded_tf[b"info"])).digest()

        self.url_para['info_hash']=self.bd.escaped_hash  (self.info_hash)

        self.url_para['uploaded']=0
        self.url_para['downloaded']=0
        self.url_para['left']=self.file_size()
        self.url_para['port']=6889
        self.url_para['compact']=1
        self.url_para['event']='started'

    def get_url(self,url_para):
        url=f"{url_para['announce']}?info_hash={url_para['info_hash']}&peer_id{url_para    ['peer_id']}&uploaded{url_para ['uploaded']}&downloaded{url_para   ['downloaded']}&left{url_para['left']}&port={url_para['port']}&compact={url_para ['compact']}&event={url_para['event']}"
        return url

    peice_count=[-1 for i in range(bitmap_length)]
    rank_count=[]



    def get_next_task(self):
        pass

    def update_peers(self):
        print(self.get_url(self.url_para))
        announce_content=requests.get(self.get_url(self.url_para)).content
        print(announce_content)
        # self.announce=self.bd.decode(announce_content)
        # self.peers=self.announce.peers

    def most_imp_func(writer,reader):
        host,port=writer.extra_info("peer")
        if host in peers:
            pass
        return something


    def request_message(index,begin,block):
        request=struct.pack('!IB',13,6,index,begin,block)
        return request

    async def download_piece(reader,writer):
        piece=bitarray()

        request=request_message()
        await writer.write(request)
        new_data=await reader.read(chunk)
        if not new_data:
            pass
        peice.extend(new_data)

    async def handle_messages(reader,writer):

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
                pass

            if message_id==8:#cancel
                pass

    async def start_torrent_client(self):
        pass
        #send handshake
        #handshake=receive handshake
        #send bitmap
        #thispeer.bitmap=receive bitmap
        #update_peers()
        #handle messagees

ubn1="ubuntu-24.04-desktop-amd64.iso.torrent"
# print(b'\x03')
# print(struct.pack('!ii',1,2))
# print(bytearray([3,2,3]))
tcs=torrent_client_side(ubn1)
print(tcs.peers)
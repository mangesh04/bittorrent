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
import bencode_decoder






class torrent_client_side:

    def __init__(self,torrent_file):
        self.bd=bencode_decoder()
        self.decoded_tf=self.bd.decode_file(torrent_file)


    def get_url(self,url_para):

        url=f"{url_para['announce']}?info_hash={url_para['info_hash']}&peer_id={url_para['peer_id']}&uploaded={url_para['uploaded']}&downloaded={url_para['downloaded']}&left={url_para['left']}&port={url_para['port']}&compact={url_para['compact']}&event={url_para['event']}"

        return url

    def get_url_parameters(self):
        self.url_para['announce'] =self.decoded_tf[b"announce"].decode()
        self.url_para['peer_id']=create_peer_id('-MT0001-')
        self.info_hash=hashlib.sha1(bd.encode(self.decoded_tf[b"info"])).digest()
        self.url_para['info_hash']=bd.escaped_hash(info_hash)
        self.url_para['uploaded']=0
        self.url_para['downloaded']=0
        self.url_para['left']=file_size(self.decoded_tf)
        self.url_para['port']=6889
        self.url_para['compact']=1
        self.url_para['event']='started'
        return url_para


    def sort_peers():
        def compare(a,b):
            if a['uploaded']<b['uploaded']:
                return 1
            else:
                return -1

        self.peers=sorted(peers,key=cmp_to_key(compare))

    def request_message(index,begin,block):
        request=struct.pack('!IB',13,6,index,begin,block)
        return request

    async def download_piece(reader,writer):
        piece=bitarray()

        request=request_message()
        await writer.write(request)
        new_data=await reader.read(chunk)
        if not new_data:
            break
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




    def set_message_schema(self):

        self.message['keep-alive']=struct.pack('!I',0) #empty four bytes message without any id
        self.message['choke']=struct.pack('!IB',1,0) #message length and id
        self.message['unchoke']=struct.pack('!IB',1,1)
        self.message['interested']=struct.pack('!IB',1,2)
        self.message['not interested']=struct.pack('!IB',1,3)

        #all the below messages are missing payloads , length may also change.
        #but it'll help for lenth and id
        self.message['have']=struct.pack('!IB',5,4)
        self.message['bitfield']=struct.pack('!IB',1,5)
        self.message['request']=struct.pack('!IB',13,6)
        self.message['piece']=struct.pack('!IB',9,7)
        self.message['cancel']=struct.pack('!IB',13,8)
        self.message['port']=struct.pack('!IB',3,9)

    def file_size(self):

        left=0
        if b"files" in self.decoded_tf[b"info"]:
            sum=0
            for i in self.decoded_tf[b"info"][b"files"]:
                sum+=i[b"length"]
            left=sum
        else:
            left=int(str(self.decoded_tf[b"info"][b"length"]).encode(),10)

        return left

    def create_peer_id(self,client_id):
        return f"{client_id}{''.join([str(random.randint(0,   9)) for _ in range(12)])}"


    def create_handshake(self,peer_id, info_hash):
        protocol_string = b"BitTorrent protocol"
        pstrlen = len(protocol_string)

        # Ensure the peer_id and info_hash are 20 bytes long
        if len(peer_id) != 20 or len(info_hash) != 20:
            raise ValueError("peer_id and info_hash must be 20 bytes long.")

        # Create the reserved bytes (8 bytes)
        reserved = b'\x00' * 8

        # Construct the handshake message
        handshake = (
            struct.pack('B', pstrlen) +   # pstrlen (1 byte)
            protocol_string +              # pstr (19 bytes)
            reserved +                     # reserved (8 bytes)
            info_hash +                  # info_hash (20 bytes)
            peer_id                        # peer_id (20 bytes)
        )

        return handshake



    # async def tcp_client(self):

    #     async def close_writer():
    #         writer.close()
    #         await writer.wait_closed()

    #     async def send_message(writer):
    #         message=await aioconsole.ainput()
    #         writer.write(message.encode())
    #         await writer.drain()

    #     async def receive_message(reader):
    #         data = await reader.read(100)
    #         return data

    #     async def connect_server(host,port):
    #         return  await asyncio.open_connection(host, port)

    #     async def download_file(host,port,chunk=16*1024):
    #         reader , writer= await connect_server(host,port)

    #         file = bytearray()

    #         while True:
    #             new_data=await reader.read(chunk)
    #             if not new_data:
    #                 break
    #             peice.extend(new_data)

    #         return file

    #     async def get_peers(self,url):
    #         async with aiohttp.ClientSession() as session:
    #             stream=await session.get(url)
    #             data=await stream.content.read()
    #             self.peers=self.bd.decode(data)

    #     async def download_pieces(self):
    #         while True:
    #             self.download_file()
    #     async def run(self):
    #         await asyncio.gather(download_pieces(),get_peers())

buk="big-buck-bunny.torrent"
ubn1="ubuntu-24.04-desktop-amd64.iso.torrent"
# tcs=torrent_client_side(ubn1)
print(b'\x03')
print(struct.pack('!ii',1,2))
print(bytearray([3,2,3]))
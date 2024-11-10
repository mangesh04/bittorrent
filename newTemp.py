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


class bencode_decoder:

    def is_int(self,char):
        return char>=ord('0') and char<=ord('9')

    def btoi(self,tstr,i=0):
        dint=b""
        i+=1
        while chr(tstr[i])!='e':
            dint+=chr(tstr[i]).encode("utf-8")
            i+=1
        return (int(dint),i)


    def btos(self,tstr,i=0):
        slen=""
        while self.is_int(tstr[i]):
            slen+=chr(tstr[i])
            i+=1
        i+=1
        dstr=""
        j=i+int(slen)
        return (tstr[i:j],j-1)


    def btol(self,tstr,i=0):
        if chr(tstr[i+1])=='e':
            return ([],i+1)
        temp,i=self.decode_helper(tstr,i+1)
        nel=[temp]
        temp2,i=self.btol(tstr,i)
        nel+=temp2
        return (nel,i)


    def btod(self,tstr,i=0):
        if chr(tstr[i+1])=='e':
            return ({},i+1)

        nel1,i=self.decode_helper(tstr,i+1)
        nel2,i=self.decode_helper(tstr,i+1)
        bdict={nel1:nel2}
        temp,i=self.btod(tstr,i)
        bdict.update(temp)
        return (bdict,i)

    def decode_helper(self,tstr,i=0):
        #i (int): The current index (pointer) in the byte string `data` where decoding begins.

        if self.is_int(tstr[i]):
            return self.btos(tstr,i)

        fc=chr(tstr[i])

        if fc=='i':
            return self.btoi(tstr,i)

        if fc=='l':
            return self.btol(tstr,i)

        if fc=='d':
            return self.btod(tstr,i)


    def escape(self,i):
        if (i>=ord('0') and i<=ord('9')) or (i>=ord('a') and i<=ord ('z')) or (i>=ord('A') and i<=ord('Z')) or i==ord('-') or    i==ord('_') or i==ord('.')or i==ord('~'):
            return chr(i)

        if i<=15:
            return hex(i).replace("0x","%0").upper()

        return hex(i).replace("0x","%").upper()

    def escaped_hash(self,hash):
        info_hash=""
        for i in hash:
            info_hash+=self.escape(i)
        return info_hash

    def print_in_format(self,ele,i=0):

        pprint.pprint(ele)
        # if isinstance(ele,dict):
        #     for key in ele:
        #         print(i*" ",key,":")
        #         self.print_in_format(ele[key],i+1)

        # if isinstance(ele,list):
        #     for val in ele:
        #         self.print_in_format(val,i+1)

        # if isinstance(ele,bytes):
        #     print(i*" ",ele)

        # if isinstance(ele,int):
        #     print(i*" ",ele)



    def decode(self,torrent_string):
        return self.decode_helper(torrent_string)[0]

    def decode_file(self,file):
        with open(file,'rb') as f:
            return self.decode(f.read())

    def encode(self,data):

        if type(data)==int:
            return f"i{data}e".encode()

        if type(data)==bytes:
            return f"{len(data)}:".encode()+data

        if type(data)==list:
            return b"l"+b"".join([self.encode(i) for i in data])+b"e"

        if type(data)==dict:
            bdict = b"d"
            for key in data:
                bdict+=self.encode(key)
                bdict+=self.encode(data[key])
            bdict+=b"e"
            return bdict







class torrent_client_side:




    def __init__(self,torrent_file):
        self.peers=[]
        self.url_para={'announce':'',
        'info_hash':'',
        'peer_id':'',
        'uploaded':'',
        'downloaded':'',
        'left':'',
        'port':'',
        'compact':'',
        'event':''}

        self.message={'keep-alive':b'',
        'choke':b'',
        'unchoke':b'',
        'interested':b'',
        'not interested':b'',
        'have':b'',
        'bitfield':b'',
        'request':b'',
        'piece':b'',
        'cancel':b'',
        'port':b''
        }
        self.bd=bencode_decoder()
        self.decoded_tf=self.bd.decode_file(torrent_file)

        self.peers_schema={
        "host":'',
        "port":'',
        "bitfild":'',
        "uploaded":'',
        }
        self.peers=[]

    def sort_peers():
        def compare(a,b):
            if a['uploaded']<b['uploaded']:
                return 1
            else:
                return -1

        self.peers=sorted(peers,key=cmp_to_key(compare))


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

    def get_url(self,url_para):

        url=f"{url_para['announce']}?info_hash={url_para['info_hash']}&peer_id={url_para['peer_id']}&uploaded={url_para['uploaded']}&downloaded={url_para['downloaded']}&left={url_para['left']}&port={url_para['port']}&compact={url_para['compact']}&event={url_para['event']}"

        return url

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
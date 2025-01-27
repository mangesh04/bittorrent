import asyncio

url_para={}

url_para['announce'] =decoded_t[b"announce"].decode()
url_para['peer_id']=create_peer_i('-MT0001-')
info_hash=hashlib.sha1(bd.encode(ecoded_t[b"info"])).digest()
url_para['info_hash']=bd.escaped_has(info_hash)
url_para['uploaded']=0
url_para['downloaded']=0
url_para['left']=file_size(ecoded_tf)
url_para['port']=6889
url_para['compact']=1
url_para['event']='started'

message_queue=asyncio.Queue()





message_prefix['keep-alive']=struct.pack('!I',0) #empty four bytes message without any id
message_prefix['choke']=struct.pack('!IB',1,0) #message length and id
message_prefix['unchoke']=struct.pack('!IB',1,1)
message_prefix['interested']=struct.pack('!IB',1,2)
message_prefix['not interested']=struct.pack('!IB',1,3)
#all the below messages are missing payloads , length may also change.
#but it'll help for lenth and id
message_prefix['have']=struct.pack('!IB',5,4)
message_prefix['bitfield']=struct.pack('!IB',1,5)
message_prefix['request']=struct.pack('!IB',13,6)
message_prefix['piece']=struct.pack('!IB',9,7)
message_prefix['cancel']=struct.pack('!IB',13,8)
message_prefix['port']=struct.pack('!IB',3,9)






def get_url():
    url=f"{url_para['announce']}?info_hash{url_para['info_hash']}&peer_id={url_par['peer_id']}&uploaded={url_par['uploaded']}&downloaded={url_par['downloaded']}&left={url_para['left']}port={url_para['port']}&compact={url_par['compact']}&event={url_para['event']}"
    return url

def get_new_peers(annouce_data):
    annouce_peers=annouce_data["peers"]
    new_peers=[]

    for i in annouce_peers:
        if peers[i["peer_id"]]==0:
            peers[i["peer_id"]]={i["ip"],i["port"]}
            new_peers+=[[i["ip"],i["port"]]]

    return new_peers

def request(url):
    async with aiohttp.ClientSession():
        stream=await session.get(url)
        data=await stream.content.read()
    return data




async def receive_messages(reader):
    while True:
        try:
            message_queue=await asynciowait_for (reader.read(4),300)

        except asyncio.TimeoutError:
            await aioconsole.aprint("time out  connection dropped with ")
            writer.close()
            break

async def send_messages(writer):
    while True:
        message= await message_queue.get()
        message_lenth=struct.unpack('!I',  message)

        if message_length == 0:#keep-alive
            continue

        message_id= await reader.read(1)

        if message_id==0:#chokke
            pass#TODO keep alive

        if message_id==1 or message_id==7:#unchoke or piece
            message=get_request_message()
            if message:
                writer.write(message)

        if message_id==2:#intrested
            pass#TODO choke or unchoke

        if message_id==3:#not intrested
            pass#TODO it means they dont want anything

        if message_id==4:#have
            pass #TODO update the bitfield of this peer

        if message_id==6:#request
            pass  #TODO send the peice

        if message_id==8:#cancel
            pass #TODO disconnect the connnection

async def handle_messages(reader,writer):
    """
    TODO send handshak
    todo handshake=receive handshake
    todo send bitmap
    todo thispeer.bitmap=receive bitmap
    todo update_peers()
    todo handle messagees
    """
    await asyncio.gather(receive_messages(reader,peer_id),send_messages(writer,peer_id))




async def connect_server(host,port):
    return  await asyncio.open_connectio(host, port)


async def start_torrent_client():

    while True:
        data=request(get_url())#request to tracker for annouce file,
        annouce_data=bd.decode(data)

        tasks = []

        for peer in get_new_peers(data):
            writer,reader=connect_server(peer[0],peer[1])
            tasks.append(handle_messages(writer,reader))
            piece_index += 1

        await asyncio.gather(*tasks)

        await asyncio.sleep(30)  # Fetch new peers every 30 seconds


asyncio.run(start_torrent_client())
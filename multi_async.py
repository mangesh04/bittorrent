import asyncio







peice_count=[-1 for i in range(bitmap_length)]#works as rarity rank
rank_count=[0 for i in range(len(peers))]
bd=bencode_decoder()
decoded_tf=bd.decode_fil(torrent_file)
peers={}
bitmap_length=9
downloaders_limit=3


def update_piece_count(peer_id,update):
    if type(update)==bytes:
        for i in len(peers["peer_id"]["bitfield"]):
            peice_count[i]+=peers["peer_id"]["bitfield"][i]

    if type(update)==int:
        peice_count[update
        ]+=peers["peer_id"]["bitfield"][update]

def update_rank_count():
    #just temparary words
    for i in peice_count:
        rank_count[i-1]+=1


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
cancel_queue=asyncio.Queue()





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
            message=await asynciowait_for (reader.read(4),300)

            if message == cancel_message:#todo just algo written
                cancel_queue.put(message)
            message_queue.put(message)

        except asyncio.TimeoutError:
            message_queue.put(message_prefix["chock"])
            await aioconsole.aprint("time out  connection dropped with ")
            writer.close()
            break

def manage_choking():
    pass

async def send_messages(writer,peer_id):
    while True:

        if not cancel_queue.empty():
            while not cancel_queue.empty():
                cancel_message=cancel_queue.get()
                for i in range(len(message_queue)):
                    message=message_queue.get()
                    if cancel_message!=message:#todo just logic and algo here
                        message_queue.put(message)

        message= await message_queue.get()
        message_lenth=struct.unpack('!I',  message)

        if message_length == 0:#keep-alive
            continue

        message_id= await reader.read(1)#TODO now we dont read message from here so change the logic like above

        if message_id==0:#chokke
            writer.write(message_prefix["keep-alive"])

        if message_id==1 or message_id==7:#unchoke or piece
            message=get_request_message()
            if message:
                writer.write(message)

        if message_id==2:#intrested
            manage_choking()

        if message_id==3:#not intrested
            pass#it means they dont want anything , dont think we have to do anything here,but it does help to understand

        if message_id==4:#have
            index=struct.unpack("need to update this liene",message)
            peers[peer_id][index]=1
            #TODO update the bitfield of this peer,check the logic again

        if message_id==6:#request /  <len=0013><id=6><index><begin><length>
            piece_index=struct.unpack("....",message)
            piece_offset=struct.unpack("....",message)
            chunck_length=struct.unpack("",message)
            #TODO send the peice,check logic and code again

async def handle_messages(reader,writer,peer_id,info_hash):

    writer.write(create_handshake(peer_id,info_hash))
    handshake=reader.read("handshake size")

    if not check_handshake(handshake):#todo have to create this function
        writer.close()#todo something is missing here
        return
    writer.write(bitmap)
    reader.read(bitmap_size)#todo give args properly
    #todo update_peers()
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


def run_client():
    asyncio.run(start_torrent_client())

#variables needed in above code are
#info_hash, peer_id, writer ,reader,bitmap
import pprint

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





def create_handshake(peer_id, info_hash):
    protocol_string = b"BitTorrent protocol"
    pstrlen = len(protocol_string)
    # Ensure the peer_id and info_hash are 20bytes long
    if len(peer_id) != 20 or len(info_hash) !=20:
        raise ValueError("peer_id and info_hashmust be 20 bytes long.")
    # Create the reserved bytes (8 bytes)
    reserved = b'\x00' * 8
    # Construct the handshake message
    handshake = (
        struct.pack('B', pstrlen) +   # pstrlen(1 byte)
        protocol_string +              # pstr(19 bytes)
        reserved +                     #reserved (8 bytes)
        info_hash +                  #info_hash (20 bytes)
        peer_id                        #peer_id (20 bytes)
    )
    return handshake

def create_peer_id(client_id):
    return f"{client_id}{''.join([str(randomrandint(0,   9)) for _ in range(12)])}"


def file_size():
    left=0
    if b"files" in decoded_tf[b"info"]:
        sum=0
        for i in decoded_tf[b"info"][b"files"]:
            sum+=i[b"length"]
        left=sum
    else:
        left=int(str(decoded_tf[b"info"][b"length"]).encode(),10)
    return left


bd=bencode_decoder()

data=bd.decode_file("announce")
bd.print_in_format(data)
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


#TODO delete these 2 functions if not essential
def bytes_to_bits(size, unit):
    unit=unit.upper()
    units_in_bits = {
        'B': 1,  # Bytes to bits
        'KB': 1024,
        'MB': 1024 * 1024,
        'GB': 1024 * 1024 * 1024,
        'TB': 1024 * 1024 * 1024 * 1024
    }

    if unit in units_in_bits:
        return size * units_in_bits[unit]
    else:
        raise ValueError("Unknown unit")



def choose_piece_size(file_size):

    piece_size = bytes_to_bits(256 ,"kb") # minimum piece size

    number_of_pieces=file_size / piece_size
    while  number_of_pieces > 1000 and piece_size <= bytes_to_bits(512,"mb"):
        piece_size *= 2
    return piece_size
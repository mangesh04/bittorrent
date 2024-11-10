import os

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

file_size = bytes_to_bits(10,"mb")
piece_size = choose_piece_size(file_size)
# print(f"Chosen piece size: {piece_size/ 1024 } KB")

file="C:\\Users\\mange\\Pictures\\Screenshot (74).png"
file_size=os.path.getsize(file)
print(file_size)
pieces=[]

with open(file,'rb') as f:
    new_data= f.read(piece_size)
    while new_data:
        pieces+=[new_data]
        new_data= f.read(piece_size)

with open('new.png','wb') as f:
    for piece in pieces:
        f.write(piece)
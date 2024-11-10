import bencodepy
import hashlib
import urllib.parse
import requests

# Step 1: Read the torrent file and decode it
with open("ubuntu-24.04-desktop-amd64.iso.torrent", 'rb') as torrent_file:
    torrent_data = torrent_file.read()

decoded_torrent = bencodepy.decode(torrent_data)

# Step 2: Extract and bencode the 'info' dictionary
info_dict = decoded_torrent[b'info']
bencoded_info = bencodepy.encode(info_dict)

# Step 3: Hash the bencoded 'info' dictionary using SHA-1
info_hash = hashlib.sha1(bencoded_info).digest()

# (Optional) Step 4: URL-encode the info_hash for use in a tracker URL
url_encoded_info_hash = urllib.parse.quote(info_hash)
# print(bencoded_info)
print("Info Hash:", info_hash)
print("URL-encoded Info Hash:", url_encoded_info_hash)

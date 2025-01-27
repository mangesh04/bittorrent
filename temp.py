import asyncio
from bitarray import bitarray
from functools import cmp_to_key

peers={"peer1":{"bitmap":bitarray("110101010")},"peer2":{"bitmap":bitarray("110101010")},"peer3":{"bitmap":bitarray("010101111")}}

bitmap_length=9
peice_count=[1,1,2,3]
rank_count=[0 for i in range(9)]

def update_rank_count():
    for i in peice_count:
        rank_count[i-1]+=1

    for i in range(bitmap_length-1):
        rank_count[i+1]+=rank_count[i]

update_rank_count()
print(rank_count)

# def sort_peers(peers):
#     sorted_peers=[]

#     for i in range(len(sorted_peers_no)):
#         if sorted_peers_no[i][0]>0:
#             for peer in peers:
#                 if peers[peer]['bitmap'][sorted_peers_no[i][1]] == 1:
#                     if not peers[peer]['bitmap'] in sorted_peers:
#                         sorted_peers+=[peers[peer]['bitmap']]

#     return sorted_peers

# print(sort_peers(peers))


# sort_peers()







# shared_var=0

# from1=0
# from2=0
# from3=0

# async def example1():
#     global from1,shared_var
#     for i in range(3):
#         from1=shared_var
#         await asyncio.sleep(0.1)
#         shared_var=from1+1
#         print("from 1",shared_var)

# async def example2():
#     global from2,shared_var
#     for i in range(3):
#         from2=shared_var
#         await asyncio.sleep(0.1)
#         shared_var=from2+1
#         print("from 2",shared_var)


# async def main():
#     # e1=asyncio.create_task(example1())
#     # e2=asyncio.create_task(example2())
#     # e3=asyncio.create_task(example3())
#     # await asyncio.gather(e1,e2,e3)
#     # await example1()
#     # await example2()
#     await asyncio.gather(example1(),example2())

# asyncio.run(main())

# print("total value",shared_var)
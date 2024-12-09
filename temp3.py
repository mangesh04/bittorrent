# objects=[{"name":"mangesh"},{"name":"omkar"},{"name":"tushar"}]

# objects={"peer1":{"number":3,"rarity":0},"peer2":{"number":2,"rarity":0}}

# def sort_rarity(objects):

import random

def bubble_sort(arr):

    for i in range(len(arr)-1):
        for j in range(len(arr)-i-1):
            if arr[j]>arr[j+1]:
                temp=arr[j]
                arr[j]=arr[j+1]
                arr[j+1]=temp
    return arr

num_arr=[random.randint(1,10) for i in range(10)]
print(num_arr)
num_arr=bubble_sort(num_arr)
print(num_arr)
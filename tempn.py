import asyncio

async def work(time,string):
    while True:
        await asyncio.sleep(time)
        print(string)

async def main():

    # for i in range(10):
    #     await asyncio.create_task(work(i))
    # tasks=[work(1,"A"),work(2,"B")]
    tasks=[]
    await asyncio.gather(*tasks)

asyncio.run(main())
import asyncio
import uuid

async def producer(q):
    ctr = 0
    while True:
        # await asyncio.sleep(0.2)
        await asyncio.sleep(0)
        ctr += 1
        # await q.put(uuid.uuid4())
        await q.put(str(ctr))

async def consumer(q, name="", slp=0.1):
    while True:
        await asyncio.sleep(slp)
        msg = await q.get()
        print(f"Consumer {name} pulled {msg}")
        # q.task_done()

async def main(loop):
    q = asyncio.Queue(maxsize=5)
    asyncio.create_task(consumer(q, "first"))
    await asyncio.gather(producer(q), consumer(q, name="second", slp=2))

try:
    loop = asyncio.get_event_loop()
    asyncio.gather(main(loop))
    loop.run_forever()
except KeyboardInterrupt:
    print("Closing loops")
finally:
    loop.close()


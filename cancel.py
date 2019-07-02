import asyncio
from datetime import datetime

async def ctask():
    asyncio.Task.current_task().name = "ctsk"
    while True:
        await asyncio.sleep(0.4)
        print(datetime.now())


async def main():
    loop = asyncio.get_event_loop()
    t = loop.create_task(ctask())
    t.name = "myname"
    print(t.name)
    await asyncio.sleep(2)
    t.cancel()



asyncio.run(main())

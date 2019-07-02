import aiohttp
import asyncio

urls = [
        "https://www.python.org",
        "https://www.google.co.in",
        "https://www.netflix.com"
        ]

async def worker(q):
    while True:
        print(await q.get())

async def fetch(session, url, q):
    async with session.get(url) as response:
        res = await response.text()
        await q.put(res)

async def main():
    q = asyncio.Queue()
    asyncio.create_task(worker(q))
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, q) for url in urls]
        await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

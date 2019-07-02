import asyncio
from aiohttp import request
from aiomultiprocess import Pool


async def get(url):
    async with request("GET", url) as response:
        return await response.text("utf-8")


async def main():
    urls = ["https://www.python.org", "https://google.co.in"]
    async with Pool() as pool:
        result = await pool.map(get, urls)
        print(result)


asyncio.run(main())

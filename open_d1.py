import asyncio
import aiohttp
import json
import dask
import dask.dataframe as dd

from pprint import pprint as pp

RESOURCE = "3e87c431-9c00-4a11-8d32-00bf9c6bd967"
API_KEY = "579b464db66ec23bdd0000015a3abe90c8dc42f44465d9b1425236e3"
OFF_MIN = 0
OFF_MAX = 1000


async def worker(session, OFF_MIN, OFF_MAX):
    url = f"https://api.data.gov.in/resource/{RESOURCE}?api-key={API_KEY}&format=json&offset={OFF_MIN}&limit={OFF_MAX}"
    header = {"accept": "application/json"}
    async with session.get(url, ssl=False, headers=header) as response:
        res = await response.text()
        ry = json.loads(res)
        # print(res)
        pp(ry["records"][0])
        df = dd.read_json(json.loads(res)).compute()
        df.head(3)
        pp(len(df))
        return res


async def main():
    async with aiohttp.ClientSession() as session:
        # tasks = [asyncio.create_task(worker(session, x, x + 1000)) for x in range(1000, 10000, 1000)]
        tasks = [asyncio.create_task(worker(session, 0, 1000))]
        await asyncio.gather(*tasks)


loop = asyncio.get_running_loop()
loop.run_until_complete(main())

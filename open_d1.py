import asyncio
import aiohttp
import json
import dask
import dask.dataframe as dd
import dask.bag as db

from pprint import pprint as pp

RESOURCE = "3e87c431-9c00-4a11-8d32-00bf9c6bd967"
API_KEY = "579b464db66ec23bdd0000015a3abe90c8dc42f44465d9b1425236e3"
OFF_MIN = 0
OFF_MAX = 1000
B_DF = None


async def worker(session, OFF_MIN, OFF_MAX):
    global B_DF
    url = f"https://api.data.gov.in/resource/{RESOURCE}?api-key={API_KEY}&format=json&offset={OFF_MIN}&limit={OFF_MAX}"
    header = {"accept": "application/json"}
    async with session.get(url, ssl=False, headers=header) as response:
        res = await response.text()
        ry = json.loads(res)
        # print(res)
        # pp(ry["records"][0])
        if B_DF is None:
            B_DF = db.from_sequence(ry["records"]).to_dataframe()
        else:
            B_DF.append(db.from_sequence(ry["records"]).to_dataframe())
        # pp(df)
        # pp(df.head(10))
        # pp(B_DF)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(worker(session, x, x + 1000)) for x in range(1000, 10000, 1000)]
        # tasks = [asyncio.create_task(worker(session, 0, 1000))]
        await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
pp(len(B_DF))

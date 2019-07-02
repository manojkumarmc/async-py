import asyncio
import random
from colorama import Fore

colors = [
    Fore.BLUE,
    Fore.CYAN,
    Fore.GREEN,
    Fore.MAGENTA,
    Fore.RED,
    Fore.WHITE,
    Fore.YELLOW
]


async def worker(cid, wname):
    print(f"Worker {wname} created")
    ctr = 0
    # stime = random.randint(1,5) / 0.7
    stime = 0.2
    while True:
        await asyncio.sleep(stime)
        ctr += 1
        print(f"{cid} Worker {wname} processing [{ctr}]")


async def main():
    print("Starting workers.....!")
    loop = asyncio.get_event_loop()
    tasks = [asyncio.create_task(worker(random.sample(colors, 1)[0], f"Name {x}")) for x in range(10)]
    await asyncio.gather(*tasks)


asyncio.run(main())


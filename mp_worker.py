import asyncio
import signal
from aiohttp import request
from aiomultiprocess import Pool


async def ask_exit(signame, loop, pool):
    print("got signal %s: exit" % signame)
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    pool.terminate()
    loop.stop()


async def worker(wname):
    asyncio.Task.current_task().name = wname
    print(f"Worker {wname} is starting")
    ctr = 0
    # while True:
    #     await asyncio.sleep(0.5)
    #     print(f"Processing in {wname}")
    await asyncio.sleep(5)
    print(f"processed {wname}")


async def main():
    async with Pool() as pool:
        loop = asyncio.get_event_loop()
        for signame in {"SIGINT", "SIGTERM"}:
            loop.add_signal_handler(
                getattr(signal, signame),
                lambda signame=signame: asyncio.create_task(
                    ask_exit(signal, loop, pool)
                ),
            )
        result = await pool.map(worker, [f"{w}-worker" for w in range(1, 4)])
        print(result)


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main(), return_exceptions=True))
except KeyboardInterrupt:
    print("Keyboard inter")
finally:
    print("Exiting....!")
    loop.close()

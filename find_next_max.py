import asyncio
import signal

from datetime import datetime


async def ask_exit(signame, loop):
    print("got signal %s: exit" % signame)
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def worker(min, max):
    while min <= max:
        await asyncio.sleep(0)
        min += 1
        print(min)


async def main():
    num = 20_170_000
    itvl = 1_000_000
    str_num = str(num)
    mx_str_num = str_num[0] + len(str_num[1:]) * "9"
    print(mx_str_num)
    stime = datetime.now().time()
    tasks = [
        asyncio.create_task(worker(x, x + itvl))
        for x in range(num, int(mx_str_num), itvl)
        if x + itvl <= int(mx_str_num)
    ]
    await asyncio.gather(*tasks)
    etime = datetime.now().time()
    print(f" {stime} {etime}")


try:
    loop = asyncio.get_event_loop()
    for signame in {"SIGINT", "SIGTERM"}:
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda signame=signame: asyncio.create_task(ask_exit(signame, loop)),
        )
    loop.run_until_complete(asyncio.gather(main(), return_exceptions=True))
finally:
    print("Exiting....!")
    loop.close()

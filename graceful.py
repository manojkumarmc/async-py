import asyncio
import signal
import functools
import uuid


async def ask_exit(signame, loop):
    print("got signal %s: exit" % signame)
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def producer(q, pname="prod1"):
    print(f"Starting producer {pname}")
    while True:
        await asyncio.sleep(0.4)
        await q.put(uuid.uuid4())


async def consumer(q, cname="cons1"):
    print(f"Started consumer {cname}")
    while True:
        await asyncio.sleep(0.4)
        print(await q.get())

q = asyncio.Queue()
try:
    loop = asyncio.get_event_loop()
    for signame in {"SIGINT", "SIGTERM"}:
        loop.add_signal_handler(
                getattr(signal, signame), lambda signame=signame: asyncio.create_task(ask_exit(signame, loop))
        )
    loop.run_until_complete(asyncio.gather(producer(q, "f"), consumer(q), return_exceptions=True))
    # loop.run_forever()
finally:
    print("Exiting....!")
    loop.close()

# q = asyncio.Queue()
# try:
#     loop = asyncio.get_event_loop()
#     loop.create_task(producer(q, "first"))
#     loop.create_task(producer(q, "second"))
#     loop.create_task(consumer(q))
#     for signame in {"SIGINT", "SIGTERM"}:
#         loop.add_signal_handler(
#                 getattr(signal, signame), lambda signame=signame: asyncio.create_task(ask_exit(signame, loop))
#         )
#     loop.run_forever()
# finally:
#     print("Exiting....!")
#     loop.close()

import asyncio
from signal import SIGINT, SIGTERM


async def main():
    try:
        while True:
            print("<Your app is running>")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        for i in range(3):
            print("<Your app is shutting down...>")
            await asyncio.sleep(1)


def handler(sig):
    loop.stop()
    print(f"Got signal: {sig!s}, shutting down.")
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)
    loop.create_task(main())
    loop.run_forever()
    tasks = asyncio.Task.all_tasks()
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()

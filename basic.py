import asyncio


async def main():
    print("Hello, world")

# try:
#     loop = asyncio.get_event_loop()
#
#
#     # asyncio.gather(main())
#     loop.create_task(main())
#
#
#     cb = lambda: asyncio.ensure_future(main())
#     loop.call_later(3, cb)
#
#
#     # loop.run_until_complete(asyncio.gather(main()))
#     loop.run_forever()
# finally:
#     loop.close()

asyncio.run(main())

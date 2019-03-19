
import time
import random
import asyncio
import aiohttp


URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


async def fetch_async(session, pid):
    start = time.time()
    sleepy_time = random.randint(2, 5)

    print('Fetch async process {} started, sleeping for {} seconds'.format(
        pid, sleepy_time
    ))

    await asyncio.sleep(sleepy_time)

    async with session.get(URL) as response:
        datetime = response.headers.get('Date')

    return 'Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start
    )


async def asynchronous():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(
            fetch_async(session, pid)) for pid in range(1, MAX_CLIENTS + 1)]

        for i, future in enumerate(asyncio.as_completed(tasks)):
            result = await future
            print('{} {}'.format('>>'*(i+1), result))

    print("Process tookL {:.2f} seconds".format(time.time() - start))


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()

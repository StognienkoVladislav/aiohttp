
import time
import asyncio
import aiohttp

from collections import namedtuple
from concurrent.futures import FIRST_COMPLETED


Service = namedtuple('Service', ('name', 'url', 'ip_attr'))


SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)


async def fetch_ip(session, service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    async with session.get(service.url) as response:
        json_response = await response.json()
        ip = json_response[service.ip_attr]

    return '{} finished with result: {}, took: {:.2f} seconds'.format(
        service.name, ip, time.time() - start
    )


async def asynchronous():

    async with aiohttp.ClientSession() as session:
        futures = [asyncio.ensure_future(
            fetch_ip(session, service)) for service in SERVICES]

        done, pending = await asyncio.wait(
            futures, return_when=FIRST_COMPLETED
        )
        print(done.pop().result())
        for future in pending:
            future.cancel()


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()

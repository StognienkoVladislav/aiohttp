
import time
import asyncio
import aiohttp
import traceback

from collections import namedtuple


Service = namedtuple('Service', ('name', 'url', 'ip_attr'))


SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'error_attr'),
    Service('broken', 'http://no-way-this-is-goin-to-work.com/json', 'ip')
)


async def fetch_ip(session, service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    try:
        async with session.get(service.url) as response:
            json_response = await response.json()
            ip = json_response[service.ip_attr]

            response.close()
            return '{} finished with result: {}, took: {:.2f} seconds'.format(
                service.name, ip, time.time() - start
            )
    except Exception:
        return '{} is unresponsive'.format(service.name)


async def asynchronous():

    async with aiohttp.ClientSession() as session:
        futures = [asyncio.ensure_future(
            fetch_ip(session, service)) for service in SERVICES]
        done, _ = await asyncio.wait(futures)

        for future in done:
            try:
                print(future.result())
            except Exception:
                print('Unexpected error: {}'.format(traceback.format_exc()))


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()

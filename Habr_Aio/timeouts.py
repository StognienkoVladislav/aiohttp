
import time
import random
import asyncio
import aiohttp
import argparse

from collections import namedtuple
from concurrent.futures import FIRST_COMPLETED


Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
)

DEFAULT_TIMEOUT = 0.1


async def fetch_ip(session, service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))
    await asyncio.sleep(random.randint(1, 3) * 0.1)

    try:
        async with session.get(service.url) as response:
            json_response = await response.json()
            ip = json_response[service.ip_attr]

            response.close()
            print('{} finished with result: {}, took: {:.2f} seconds'.format(
                service.name, ip, time.time() - start
            ))
            return ip

    except Exception:
        return '{} is unresponsive'.format(service.name)


async def asynchronous(timeout):

    response = {
        'message': 'Result from asynchronous.',
        'ip': 'not available'
    }

    async with aiohttp.ClientSession() as session:
        futures = [asyncio.ensure_future(
            fetch_ip(session, service)) for service in SERVICES]

        done, pending = await asyncio.wait(
            futures, timeout=timeout, return_when=FIRST_COMPLETED
        )

        for future in pending:
            future.cancel()
        for future in done:
            response['ip'] = future.result()
    print(response)


parser = argparse.ArgumentParser()
parser.add_argument(
    '-t', '--timeout',
    help='Timeout to use, defaults to {}'.format(DEFAULT_TIMEOUT),
    default=DEFAULT_TIMEOUT, type=float
)
args = parser.parse_args()


print('Using a {} timeout'.format(args.timeout))
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous(args.timeout))
ioloop.close()

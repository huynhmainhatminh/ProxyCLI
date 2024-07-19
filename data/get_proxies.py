import asyncio
import aiohttp
import re
import random
from data.extra import *

all_proxy = []


async def run_getproxy(urls, amount_proxy):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            if len(list(set(all_proxy))) >= amount_proxy:
                return
            else:
                async with session.get(urls) as response:
                    proxy = await response.text()
                    response = proxy.strip().split('\n')

                    for proxies in response:
                        if len(list(set(all_proxy))) >= amount_proxy:
                            break
                        proxy_search = re.compile("^[\d]{1,3}[\W]+[\d]{1,3}[\W]+[\d]{1,3}[\W]+[\d]{1,3}:[\d]{2,5}$")
                        proxy_all = proxy_search.search(proxies)
                        if proxy_all is not None:
                            if len(list(set(all_proxy))) >= amount_proxy:
                                break
                            else:
                                all_proxy.append(proxy_all.group(0))
        except(aiohttp.client_exceptions.ClientConnectorError, aiohttp.client_exceptions.ServerDisconnectedError):
            pass


async def fetch_all(amount_proxy):
    tasks = []
    link_proxy = open("data/urls.txt").read().strip().split("\n")
    random.shuffle(link_proxy)
    for link in link_proxy:
        task = asyncio.create_task(run_getproxy(link, amount_proxy))
        tasks.append(task)
    await asyncio.gather(*tasks)
    with open('data/proxies.txt', 'w') as f:
        for _ in list(set(all_proxy)):
            f.write(_ + "\n")
    print(f"\n{yellow}[{red}!{yellow}] {medium_spring_green}GET SUCCESSFULLY {amount_proxy} PROXIES{bold}")
    sleep(5)


async def get_proxy():
    print("\n")
    logo.logo()
    amount_proxy: int = 1000
    while True:
        try:
            run(f"\n{bold}{yellow}[{cyan}●{yellow}] {sky_blue2}ENTER THE NUMBER OF PROXIES {yellow}({red}minium "
                f"{bold}= {red}10000{yellow}){bold}: ")
            amount_proxy = int(input())
            if amount_proxy < 10000:
                error_input()
            else:
                break
        except(ValueError, ):
            continue
    await fetch_all(amount_proxy)


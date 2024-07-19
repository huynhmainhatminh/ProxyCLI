import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector


class CheckerProxies:
    def __init__(self, host: str, port: int, url: str, timeout: int, retries: int, keywords, proxytype: str) -> None:
        self.host: str = host
        self.port: int = port
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.url: str = url
        self.retries: int = retries
        self.keywords = keywords
        self.proxytype: str = proxytype   # http, socks4, socks5

    async def check_response(self, session: aiohttp.ClientSession) -> int:
        try:
            async with session.get("http://azenv.net/") as response:
                content = await response.text()

                if self.host in content:
                    return 1  # transparent

                privacy_headers = ["HTTP_X_FORWARDED_FOR", "HTTP_FORWARDED", "HTTP_VIA", "HTTP_X_PROXY_ID"]

                if any([header in content for header in privacy_headers]):
                    return 2  # anonymous

                return 3  # elite
        except (Exception,):
            return 0

    async def run(self) -> int:
        for _ in range(self.retries):
            try:
                async with aiohttp.ClientSession(
                        connector=ProxyConnector.from_url(f'{self.proxytype}://{self.host}:{self.port}'),
                        timeout=self.timeout,
                        skip_auto_headers=["User-Agent"],
                ) as session:
                    async with session.get(self.url) as response:
                        if self.keywords is None:
                            if response.status == 200:
                                return await self.check_response(session)
                        else:
                            content = await response.text()
                            if any(keyword in str(content) for keyword in self.keywords):
                                return await self.check_response(session)

            except (Exception, ):
                await asyncio.sleep(0.250)
        return 0


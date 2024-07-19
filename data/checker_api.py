import asyncio
import json
from aiohttp import ClientSession


class CheckAPI:
    def __init__(self, host: str, session: ClientSession):
        self.host = host
        self.semaphore = asyncio.Semaphore(1500)
        self.session = session

    async def fetch_fraud_score(self):
        async with self.semaphore:
            async with self.session.get(f"https://web.api-bdc.io/api/Public/relay?route=10036&paramsString=ip%3D{self.host}&lang=en") as response:
                response_text = await response.text()
                if "High" in response_text:
                    return 3  # High
                elif "Moderate" in response_text:
                    return 2  # Moderate
                else:
                    return 1  # Low

    async def fetch_data_proxy(self):
        async with self.semaphore:
            async with self.session.get(f"https://web.api-bdc.io/api/Public/relay?route=10033&paramsString=ip%3D{self.host}&lang=en") as response:
                data = json.loads(await response.text())['securityThreat']
                if "PROXY" in data:
                    return 1  # PROXY
                elif "hosting" in data:
                    return 2  # hosting
                elif "unknown" in data:
                    return 3  # unknown
                elif "blacklisted" in data:
                    return 4  # blacklisted
                elif "unreachable" in data:
                    return 5  # unreachable
                elif "TOR" in data:
                    return 6  # Tor
                elif "SPAMHAUS" in data:
                    return 7  # SPAMHAUS
                else:
                    return 8  # router



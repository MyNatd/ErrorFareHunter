# scraper_core.py

import random
import aiohttp
import asyncio
import os

# Random User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)...",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F)...",
    # เพิ่มได้อีกเยอะ
]

PROXY_LIST = os.getenv('PROXY_LIST', "").split(",")  # ใส่ Proxy Server เช่น "http://proxy1.com:8080,http://proxy2.com:8080"

async def fetch_url(session, url, params=None, headers=None, retries=3):
    """Fetch URL with retry logic."""
    if headers is None:
        headers = {}

    headers['User-Agent'] = random.choice(USER_AGENTS)

    proxy = random.choice(PROXY_LIST) if PROXY_LIST else None

    for attempt in range(retries):
        try:
            async with session.get(url, params=params, headers=headers, proxy=proxy, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Attempt {attempt}: HTTP {response.status}")
        except Exception as e:
            print(f"Attempt {attempt}: {e}")
        await asyncio.sleep(2 ** attempt)  # Backoff

    return None

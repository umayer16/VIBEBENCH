import asyncio
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

async def fetch_url(url, timeout=10):
    # HUMAN TOUCH: Explicit timeout, clean error handling, returns None on failure
    if not AIOHTTP_AVAILABLE:
        return None, "aiohttp not installed"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                response.raise_for_status()
                content = await response.text()
                return content, None
    except asyncio.TimeoutError:
        return None, "Request timed out"
    except aiohttp.ClientResponseError as e:
        return None, f"HTTP error {e.status}"
    except aiohttp.ClientError as e:
        return None, f"Connection error: {e}"

if __name__ == "__main__":
    async def main():
        content, error = await fetch_url('https://httpbin.org/get')
        if error:
            print(f"Error: {error}")
        else:
            print(f"Success: {len(content)} bytes received")
    asyncio.run(main())

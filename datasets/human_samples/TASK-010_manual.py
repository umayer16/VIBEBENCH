import asyncio


async def fetch_url(url, timeout=5):
    # HUMAN TOUCH: Guard against missing aiohttp with a clear error
    try:
        import aiohttp
    except ImportError:
        return {"error": "aiohttp not installed — run: pip install aiohttp"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                if response.status >= 400:
                    return {
                        "error": f"HTTP {response.status}",
                        "url": url
                    }
                text = await response.text()
                return {
                    "url": url,
                    "status": response.status,
                    "length": len(text)
                }
    except asyncio.TimeoutError:
        return {"error": f"Timeout after {timeout}s", "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}


if __name__ == "__main__":
    result = asyncio.run(fetch_url("https://httpbin.org/get"))
    print(result)

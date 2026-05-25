import asyncio
import aiohttp
from typing import Optional

async def fetch_url_content(url: str) -> Optional[str]:
    """
    Fetches the text content of a URL with comprehensive error handling.
    """
    # Define a timeout to prevent the function from hanging indefinitely
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                # Raises ClientResponseError for 4xx and 5xx status codes
                response.raise_for_status()

                return await response.text()

    except aiohttp.ClientResponseError as e:
        print(f"HTTP Error {e.status}: {e.message} for {url}")
    except aiohttp.ClientConnectorError as e:
        print(f"Connection Error: Could not connect to {url}. Details: {e}")
    except asyncio.TimeoutError:
        print(f"Timeout Error: The request for {url} timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

# Usage example:
# content = asyncio.run(fetch_url_content("https://api.example.com/data"))

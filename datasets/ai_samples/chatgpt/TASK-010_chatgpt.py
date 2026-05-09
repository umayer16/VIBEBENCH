import asyncio
from typing import Optional

import aiohttp


async def fetch_url(
    url: str,
    timeout_seconds: int = 10,
) -> Optional[str]:
    """
    Fetch the content of a URL asynchronously using aiohttp.

    Handles:
    - Connection errors
    - Request timeouts
    - HTTP error status codes

    Returns:
        Response text on success, or None on failure.
    """

    timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:

                # Raise exception for 4xx / 5xx responses
                response.raise_for_status()

                return await response.text()

    except aiohttp.ClientResponseError as e:
        print(f"HTTP error: {e.status} - {e.message}")

    except aiohttp.ClientConnectorError as e:
        print(f"Connection error: {e}")

    except asyncio.TimeoutError:
        print(f"Request timed out after {timeout_seconds} seconds")

    except aiohttp.ClientError as e:
        # Catch any other aiohttp-related errors
        print(f"Client error: {e}")

    except Exception as e:
        # Catch unexpected errors
        print(f"Unexpected error: {e}")

    return None


# Example usage
async def main():
    url = "https://example.com"

    content = await fetch_url(url)

    if content:
        print("Fetched content successfully:")
        print(content[:200])  # Print first 200 characters


if __name__ == "__main__":
    asyncio.run(main())
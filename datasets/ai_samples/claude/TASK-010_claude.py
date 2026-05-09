import aiohttp
import asyncio
from typing import Optional

async def fetch_url(
    url: str,
    timeout_seconds: float = 10.0,
    headers: Optional[dict] = None
) -> dict:
    """
    Asynchronously fetch the content of a URL with graceful error handling.

    Args:
        url:             The URL to fetch.
        timeout_seconds: Max seconds to wait for a response (default 10).
        headers:         Optional HTTP headers to include in the request.

    Returns:
        A dict with keys:
        - success  (bool)
        - status   (int | None)
        - content  (str | None)
        - error    (str | None)
    """
    timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=timeout) as response:
                # Raise an exception for 4xx / 5xx status codes
                response.raise_for_status()

                content = await response.text()
                return {
                    "success": True,
                    "status":  response.status,
                    "content": content,
                    "error":   None,
                }

    except aiohttp.ClientResponseError as e:
        # HTTP error status codes (4xx, 5xx)
        return {
            "success": False,
            "status":  e.status,
            "content": None,
            "error":   f"HTTP error {e.status}: {e.message}",
        }

    except aiohttp.ClientConnectionError as e:
        # DNS failure, refused connection, etc.
        return {
            "success": False,
            "status":  None,
            "content": None,
            "error":   f"Connection error: {e}",
        }

    except asyncio.TimeoutError:
        # Request exceeded timeout_seconds
        return {
            "success": False,
            "status":  None,
            "content": None,
            "error":   f"Request timed out after {timeout_seconds}s",
        }

    except aiohttp.ClientError as e:
        # Catch-all for any other aiohttp-specific errors
        return {
            "success": False,
            "status":  None,
            "content": None,
            "error":   f"Client error: {e}",
        }
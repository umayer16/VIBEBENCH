import aiohttp
import asyncio
from typing import Optional


async def fetch_url(
    url: str, 
    timeout: int = 30,
    max_redirects: int = 10
) -> Optional[str]:
    """
    Asynchronously fetches content from a URL with proper error handling.
    
    Args:
        url: The URL to fetch
        timeout: Total timeout in seconds
        max_redirects: Maximum number of redirects to follow
    
    Returns:
        The response text if successful, None otherwise
    """
    try:
        # Configure timeout
        timeout_obj = aiohttp.ClientTimeout(
            total=timeout,
            connect=10,      # Connection timeout
            sock_read=20     # Read timeout
        )
        
        # Create session with timeout settings
        async with aiohttp.ClientSession(
            timeout=timeout_obj
        ) as session:
            
            async with session.get(url, max_redirects=max_redirects) as response:
                # Handle HTTP error status codes
                if response.status >= 400:
                    print(f"HTTP Error {response.status} for {url}")
                    # You can choose to raise or return None
                    # response.raise_for_status()  # Uncomment to raise on 4xx/5xx
                    return None
                
                # Get the content
                content = await response.text()
                return content
                
    except aiohttp.ClientConnectorError:
        print(f"Connection error: Could not connect to {url}")
        return None
        
    except asyncio.TimeoutError:
        print(f"Timeout error: Request to {url} timed out after {timeout}s")
        return None
        
    except aiohttp.ClientResponseError as e:
        print(f"Response error: {e.status} - {e.message}")
        return None
        
    except aiohttp.InvalidURL:
        print(f"Invalid URL: {url}")
        return None
        
    except Exception as e:
        print(f"Unexpected error fetching {url}: {e}")
        return None
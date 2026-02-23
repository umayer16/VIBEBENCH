import ssl
import socket
from datetime import datetime

def check_ssl_expiry(hostname, port=443, timeout=5):
    """
    Checks if the SSL certificate of a given hostname is expired.
    
    Args:
        hostname (str): The domain name to check.
        port (int): The port to connect to (default 443).
        timeout (int): Connection timeout in seconds.
        
    Returns:
        bool: True if the certificate is expired, False otherwise.
        dict: A dictionary containing certificate info (expiry date, status).
    """
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get certificate in dictionary format
                cert = ssock.getpeercert()
                
                # Expiry date format: 'Feb 10 23:59:59 2026 GMT'
                expire_date_str = cert.get('notAfter')
                expiry_date = datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')
                
                is_expired = datetime.utcnow() > expiry_date
                
                return is_expired, {
                    "hostname": hostname,
                    "expiry_date": expiry_date,
                    "is_expired": is_expired
                }
    except Exception as e:
        return None, {"error": str(e)}

if __name__ == "__main__":
    target_host = "google.com"
    print(f"Checking SSL certificate for: {target_host}...")
    
    expired, info = check_ssl_expiry(target_host)
    
    if expired is None:
        print(f"Error: {info['error']}")
    else:
        status = "EXPIRED" if expired else "VALID"
        print(f"Status: {status}")
        print(f"Expiry Date: {info['expiry_date']}")
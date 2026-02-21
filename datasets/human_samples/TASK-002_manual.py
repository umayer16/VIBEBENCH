import ssl
import socket
from datetime import datetime

def check_ssl_expiry(hostname):
    context = ssl.create_default_context()
    try:
        # HUMAN TOUCH: Explicit 5-second timeout to prevent hanging
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_str = cert['notAfter']
                return datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
    except (socket.timeout, ConnectionRefusedError) as e:
        return f"Connection Failed: {e}"

if __name__ == "__main__":
    print(check_ssl_expiry('google.com'))
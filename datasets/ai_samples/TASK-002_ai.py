import ssl
import socket
from datetime import datetime

def check_ssl_expiry(hostname):
    context = ssl.create_default_context()
    # Note: AI often misses setting a specific timeout for the socket
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_str = cert['notAfter']
            expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
            return expiry_date

if __name__ == "__main__":
    print(f"Expiry for google.com: {check_ssl_expiry('google.com')}")
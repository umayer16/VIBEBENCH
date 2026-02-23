import socket
import ssl
from datetime import datetime


def get_ssl_expiry_date(hostname, port=443, timeout=8):
    """
    Connects to the host via SSL and returns the certificate's notAfter date.
    Returns None if connection fails or certificate cannot be retrieved.
    
    Args:
        hostname (str): Domain name (e.g. 'google.com')
        port (int): Usually 443 for HTTPS
        timeout (int): Socket timeout in seconds
    
    Returns:
        datetime.datetime or None
    """
    try:
        # Create a standard TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Wrap socket with SSL
        context = ssl.create_default_context()
        # We don't verify hostname here because we're only interested in getting cert
        # (most servers send the cert even if hostname doesn't match)
        ssl_sock = context.wrap_socket(sock, server_hostname=hostname)
        
        # Connect
        ssl_sock.connect((hostname, port))
        
        # Get the certificate in DER format
        cert = ssl_sock.getpeercert(binary_form=True)
        
        # Close connection
        ssl_sock.close()
        
        # Parse the certificate (returns dict with 'notAfter' field)
        cert_info = ssl.DER_cert_to_PEM_cert(cert)
        pem_cert = ssl.PEM_cert_to_DER_cert(cert_info)  # not needed, but for clarity
        
        # Actually get the parsed certificate dictionary
        parsed_cert = ssl.getpeercert(ssl_sock, binary_form=False)
        
        # 'notAfter' is in format: 'MMM DD HH:MM:SS YYYY GMT'
        expiry_str = parsed_cert['notAfter']
        
        # Parse the date string
        expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
        
        return expiry_date
    
    except socket.timeout:
        print(f"Timeout connecting to {hostname}:{port}")
        return None
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
        return None
    except ConnectionRefusedError:
        print(f"Connection refused to {hostname}:{port}")
        return None
    except socket.gaierror:
        print(f"Name resolution failed for {hostname}")
        return None
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        return None
    finally:
        if 'ssl_sock' in locals():
            try:
                ssl_sock.close()
            except:
                pass
        if 'sock' in locals():
            try:
                sock.close()
            except:
                pass


def days_until_expiry(expiry_date):
    if expiry_date is None:
        return None
    now = datetime.utcnow()
    delta = expiry_date - now
    return delta.days


if __name__ == "__main__":
    test_hosts = [
        "google.com",
        "expired.badssl.com",
        "self-signed.badssl.com",
        "unreachable.example.invalid"
    ]
    
    print("SSL Certificate Expiry Check\n" + "="*30 + "\n")
    
    for host in test_hosts:
        print(f"Checking: {host}")
        expiry = get_ssl_expiry_date(host, timeout=6)
        
        if expiry:
            days_left = days_until_expiry(expiry)
            status = "EXPIRED" if days_left < 0 else "VALID"
            print(f"  → Expires: {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  → Days left: {days_left} ({status})")
        else:
            print("  → Could not retrieve certificate")
        
        print("-" * 50)
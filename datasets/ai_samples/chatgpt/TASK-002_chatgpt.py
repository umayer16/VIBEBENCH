import ssl
import socket
from datetime import datetime


def check_ssl_expiry(hostname, port=443, timeout=5):
    """
    Checks whether the SSL certificate of a given hostname is expired.

    :param hostname: The domain name (e.g., 'google.com')
    :param port: Port number (default 443)
    :param timeout: Connection timeout in seconds
    :return: Tuple (is_expired: bool, expiry_date: datetime or None, error: str or None)
    """
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        if not cert or "notAfter" not in cert:
            return None, None, "Unable to retrieve certificate expiration date."

        expiry_str = cert["notAfter"]
        expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")

        is_expired = datetime.utcnow() > expiry_date
        return is_expired, expiry_date, None

    except socket.timeout:
        return None, None, "Connection timed out."
    except ssl.SSLError as e:
        return None, None, f"SSL error: {e}"
    except socket.gaierror:
        return None, None, "Invalid hostname or DNS resolution failed."
    except Exception as e:
        return None, None, f"Unexpected error: {e}"


if __name__ == "__main__":
    test_host = "google.com"
    print(f"Checking SSL certificate for: {test_host}\n")

    expired, expiry_date, error = check_ssl_expiry(test_host)

    if error:
        print(f"Error: {error}")
    else:
        print(f"Certificate Expiry Date (UTC): {expiry_date}")
        if expired:
            print("Status: The SSL certificate is EXPIRED.")
        else:
            print("Status: The SSL certificate is VALID (not expired).")
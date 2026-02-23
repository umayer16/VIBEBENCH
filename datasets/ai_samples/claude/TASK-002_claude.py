import ssl
import socket
from datetime import datetime


def check_ssl_certificate(hostname, port=443, timeout=5):
    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        expire_date_str = cert["notAfter"]
        expire_date = datetime.strptime(expire_date_str, "%b %d %H:%M:%S %Y %Z")
        now = datetime.utcnow()

        is_expired = now > expire_date
        days_remaining = (expire_date - now).days

        return {
            "hostname": hostname,
            "expired": is_expired,
            "expiry_date": expire_date.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "days_remaining": days_remaining if not is_expired else 0,
            "days_overdue": abs(days_remaining) if is_expired else 0,
        }

    except socket.timeout:
        return {"hostname": hostname, "error": "Connection timed out"}
    except socket.gaierror:
        return {"hostname": hostname, "error": "Failed to resolve hostname"}
    except ssl.SSLCertVerificationError as e:
        return {"hostname": hostname, "error": f"SSL verification error: {e}"}
    except ssl.SSLError as e:
        return {"hostname": hostname, "error": f"SSL error: {e}"}
    except ConnectionRefusedError:
        return {"hostname": hostname, "error": "Connection refused"}
    except Exception as e:
        return {"hostname": hostname, "error": f"Unexpected error: {e}"}


def print_result(result):
    print(f"\nHostname : {result['hostname']}")
    if "error" in result:
        print(f"Error    : {result['error']}")
    else:
        status = "EXPIRED" if result["expired"] else "VALID"
        print(f"Status   : {status}")
        print(f"Expires  : {result['expiry_date']}")
        if result["expired"]:
            print(f"Overdue  : {result['days_overdue']} day(s)")
        else:
            print(f"Days Left: {result['days_remaining']} day(s)")


if __name__ == "__main__":
    hostname = "google.com"
    result = check_ssl_certificate(hostname)
    print_result(result)
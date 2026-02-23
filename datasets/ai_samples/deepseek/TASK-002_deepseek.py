import ssl
import socket
from datetime import datetime
import sys


def check_ssl_certificate_expiry(url, port=443, timeout=5):
    """
    Check if the SSL certificate for a given URL is expired.
    
    Args:
        url: The URL or hostname to check
        port: The port to connect to (default 443 for HTTPS)
        timeout: Connection timeout in seconds
        
    Returns:
        dict: Dictionary containing certificate information including:
            - 'expired': Boolean indicating if certificate is expired
            - 'expiry_date': Datetime of certificate expiry
            - 'valid_days': Days until expiry (negative if expired)
            - 'issuer': Certificate issuer
            - 'subject': Certificate subject
            - 'error': Error message if any
    """
    result = {
        'expired': None,
        'expiry_date': None,
        'valid_days': None,
        'issuer': None,
        'subject': None,
        'error': None
    }
    
    # Remove protocol prefix if present
    hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
    
    try:
        # Create a socket and wrap it with SSL
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get certificate information
                cert = ssock.getpeercert()
                
                # Extract certificate details
                result['issuer'] = dict(x[0] for x in cert['issuer'])
                result['subject'] = dict(x[0] for x in cert['subject'])
                
                # Parse expiry date
                expiry_str = cert['notAfter']
                expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                result['expiry_date'] = expiry_date
                
                # Calculate days until expiry
                now = datetime.now()
                days_until_expiry = (expiry_date - now).days
                result['valid_days'] = days_until_expiry
                
                # Check if expired
                result['expired'] = days_until_expiry < 0
                
    except socket.timeout:
        result['error'] = f"Connection timeout after {timeout} seconds"
    except socket.gaierror:
        result['error'] = f"Could not resolve hostname: {hostname}"
    except socket.error as e:
        result['error'] = f"Socket error: {str(e)}"
    except ssl.SSLError as e:
        result['error'] = f"SSL error: {str(e)}"
    except Exception as e:
        result['error'] = f"Unexpected error: {str(e)}"
    
    return result


def format_certificate_info(result):
    """
    Format certificate information for display.
    
    Args:
        result: Dictionary returned by check_ssl_certificate_expiry
        
    Returns:
        str: Formatted string with certificate information
    """
    if result['error']:
        return f"❌ Error: {result['error']}"
    
    lines = []
    
    # Status icon based on expiration
    if result['expired']:
        lines.append("❌ CERTIFICATE EXPIRED!")
    else:
        days = result['valid_days']
        if days < 7:
            lines.append(f"⚠️  Warning: Certificate expires in {days} days!")
        elif days < 30:
            lines.append(f"ℹ️  Certificate expires in {days} days")
        else:
            lines.append("✅ Certificate is valid")
    
    # Add details
    if result['expiry_date']:
        expiry_str = result['expiry_date'].strftime('%Y-%m-%d %H:%M:%S')
        lines.append(f"   Expiry date: {expiry_str}")
    
    if result['valid_days'] is not None:
        days = result['valid_days']
        if days >= 0:
            lines.append(f"   Days remaining: {days}")
        else:
            lines.append(f"   Days expired: {abs(days)}")
    
    if result['issuer']:
        issuer_str = result['issuer'].get('commonName', 'Unknown')
        lines.append(f"   Issuer: {issuer_str}")
    
    if result['subject']:
        subject_str = result['subject'].get('commonName', 'Unknown')
        lines.append(f"   Subject: {subject_str}")
    
    return '\n'.join(lines)


if __name__ == "__main__":
    print("SSL Certificate Expiry Checker")
    print("=" * 50)
    
    # Test with google.com
    test_url = "google.com"
    print(f"\nChecking certificate for: {test_url}")
    print("-" * 40)
    
    result = check_ssl_certificate_expiry(test_url)
    print(format_certificate_info(result))
    
    # Test with timeout (example with a slow server if needed)
    print("\n" + "=" * 50)
    print("Testing with different parameters:")
    print("-" * 40)
    
    # Test with a different port (if needed, uncomment below)
    # test_url_2 = "example.com"
    # result_2 = check_ssl_certificate_expiry(test_url_2, timeout=3)
    # print(format_certificate_info(result_2))
    
    # Demonstrate error handling with invalid URL
    print("\nTesting error handling (invalid URL):")
    invalid_url = "this-is-not-a-real-website-12345.com"
    result_invalid = check_ssl_certificate_expiry(invalid_url)
    print(format_certificate_info(result_invalid))
    
    # Quick summary
    print("\n" + "=" * 50)
    print("Usage tips:")
    print("- Adjust timeout parameter for slow connections")
    print("- Specify port if needed (default is 443)")
    print("- Remove http:// or https:// prefixes automatically")
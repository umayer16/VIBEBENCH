import ssl
import socket
from datetime import datetime

def check_ssl_certificate(url):
    hostname = url.replace("https://", "").replace("http://", "").split('/')[0]
    port = 443
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
            x509_cert = ssl.DER_cert_to_PEM_cert(der_cert)
            cert_lines = x509_cert.splitlines()
            cert_dates = [line for line in cert_lines if 'notAfter' in line or 'notBefore' in line]
            not_after = [date for date in cert_dates if 'notAfter' in date][0].split('=')[1]
            not_before = [date for date in cert_dates if 'notBefore' in date][0].split('=')[1]

            not_after_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            not_before_date = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
            current_date = datetime.now()

            if current_date > not_after_date:
                return f"The SSL certificate for {url} has expired on {not_after_date}."
            elif current_date < not_before_date:
                return f"The SSL certificate for {url} is not yet valid. It will be valid from {not_before_date}."
            else:
                return f"The SSL certificate for {url} is valid until {not_after_date}."

print(check_ssl_certificate("https://example.com"))
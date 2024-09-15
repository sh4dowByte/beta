import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
import ssl
import socket
from pprint import pprint

# Disable InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

metadata = {
    'description': '''
        Get SSL Cert
    ''',
    'author': 'sh4dowByte',
    'license': 'BETA',
    'portrule': ['https',],
}

def get_ssl_cert_info(hostname, port=443):
    try:
        # Membuat koneksi ke server
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Mendapatkan sertifikat
                cert = ssock.getpeercert()
                return cert
    except Exception as e:
        return (f"[red]Error: {e}[/red]")

def print_cert_info(cert):
    if cert:
        return (cert)
    else:
        return ("[yellow]No certificate found.[/yellow]")


def run(ip, port, options):
    try:
        hostname = ip
        cert_info = get_ssl_cert_info(hostname)
        cert_info = print_cert_info(cert_info)

        if isinstance(cert_info, dict):
            info_string = (
                f"Subject: {'; '.join(f'{x[0][0]}: {x[0][1]}' for x in cert_info['subject'])}\n"
                f"Issuer: {'; '.join(f'{x[0][0]}: {x[0][1]}' for x in cert_info['issuer'])}\n"
                f"Version: {cert_info['version']}\n"
                f"Serial Number: {cert_info['serialNumber']}\n"
                f"Not Before: {cert_info['notBefore']}\n"
                f"Not After: {cert_info['notAfter']}\n"
                f"Subject Alternative Names: {', '.join(f'{x[0]}: {x[1]}' for x in cert_info['subjectAltName'])}\n"
                f"OCSP URL: {', '.join(cert_info['OCSP'])}\n"
                f"CA Issuers URL: {', '.join(cert_info['caIssuers'])}\n"
                f"CRL Distribution Points: {', '.join(cert_info['crlDistributionPoints'])}"
            )
        
            return info_string
        
        return cert_info
    except Exception as e:
        return f"[red]Error: {str(e)}[/red]"
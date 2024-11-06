from datetime import datetime
import OpenSSL
import ssl
import socket
from app.utils.script import Text

metadata = {
    'description': '''
        Get SSL Cert
    ''',
    'author': 'sh4dowByte',
    'license': 'BETA',
    'portrule': ['https',],
}

def format_certificate_info(cert_info):
    """
    Format the certificate information into a human-readable string.
    
    Args:
        cert_info (dict): A dictionary containing certificate details.
        
    Returns:
        str: Formatted certificate information.
    """
    # Extracting the subject details
    subject = cert_info['Subject']
    issuer = cert_info['Issuer']
    
    # Constructing the subject information string
    subject_info = f"""Certificate Subject:
    - Country        : {subject.get(b'C', b'N/A').decode('utf-8')}
    - State/Province : {subject.get(b'ST', b'N/A').decode('utf-8')}
    - Locality       : {subject.get(b'L', b'N/A').decode('utf-8')}
    - Organization   : {subject.get(b'O', b'N/A').decode('utf-8')}
    - Common Name    : {subject.get(b'CN', b'N/A').decode('utf-8')}
    """

    # Constructing the issuer information string
    issuer_info = f"""
    Certificate Issuer:
    - Country        : {issuer.get(b'C', b'N/A').decode('utf-8')}
    - Organization   : {issuer.get(b'O', b'N/A').decode('utf-8')}
    - Common Name    : {issuer.get(b'CN', b'N/A').decode('utf-8')}
    """
    
    # Extracting additional certificate details
    serial_number = cert_info.get('Serial Number', 'N/A')
    valid_from = cert_info.get('Valid From', 'N/A')
    valid_to = cert_info.get('Valid To', 'N/A')
    # valid_to_formatted = valid_to.strftime("%Y-%m-%d %H:%M:%S")
    days_until_expiration = (datetime.now() - datetime.strptime(valid_to, "%Y%m%d%H%M%SZ")).days

    valid_from = datetime.strptime(valid_from, "%Y%m%d%H%M%SZ").strftime("%Y-%m-%d %H:%M:%S")
    valid_to = datetime.strptime(valid_to, "%Y%m%d%H%M%SZ").strftime("%Y-%m-%d %H:%M:%S")

    # Calculate days until expiration

    
    # Constructing the additional certificate details string
    other_info = f"""
    Serial Numbe     : {serial_number}
    Valid From       : {valid_from}
    Valid To         : {valid_to}
    Days Expiration  : {days_until_expiration} days
    """
    
    # Combine all the information into a single readable format
    certificate_info = subject_info + issuer_info + other_info

    return Text.remove_indentation(certificate_info)

def get_certificate_details(ip, port=443):
    """
    Retrieve and parse the SSL certificate details from a server.
    
    Args:
        ip (str): The IP address of the server.
        port (int): The port number to connect to (default is 443 for HTTPS).
        
    Returns:
        dict: A dictionary containing certificate details or an error message.
    """
    # Create an SSL context to handle the connection
    context = ssl.create_default_context()
    
    # Disable hostname checking because we're using an IP address
    context.check_hostname = False
    
    # Allow insecure connections for testing purposes
    context.verify_mode = ssl.CERT_NONE
    
    try:
        # Create a socket connection and wrap it with the SSL context
        with socket.create_connection((ip, port), timeout=30) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                # Retrieve the certificate in DER format
                der_cert = ssock.getpeercert(binary_form=True)
                
                # Load the certificate using OpenSSL
                x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, der_cert)
                
                # Extract details from the certificate
                subject = x509.get_subject()
                issuer = x509.get_issuer()
                serial_number = x509.get_serial_number()
                valid_from = x509.get_notBefore().decode('utf-8')
                valid_to = x509.get_notAfter().decode('utf-8')

                # Create a dictionary with the extracted certificate details
                cert_details = {
                    "Subject": dict(subject.get_components()),
                    "Issuer": dict(issuer.get_components()),
                    "Serial Number": serial_number,
                    "Valid From": valid_from,
                    "Valid To": valid_to,
                }
                
                return cert_details
    except Exception as e:
        return f"[red]Error: {e}[/red]"

def run(ip, port, options):
    """
    Main function to retrieve and format certificate details.
    
    Args:
        ip (str): The IP address of the server.
        port (int): The port number to connect to.
        options (dict): Additional options (not used in this function).
        
    Returns:
        str: Formatted certificate information or an error message.
    """
    try:
        # Retrieve certificate details from the server
        cert_info = get_certificate_details(ip)

        # Format the certificate details if retrieval was successful
        if isinstance(cert_info, dict):
            return format_certificate_info(cert_info)
          
        return cert_info
    except Exception as e:
        return f"[red]Error: {str(e)}[/red]"

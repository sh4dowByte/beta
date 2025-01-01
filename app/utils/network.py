import ipaddress
import os
import socket
import ssl
import sys
from app.utils.style import Colors

def ipman(targets):
    """
    Processes a list of targets (files, URLs, IP addresses, CIDR notations, or IP ranges) 
    and returns a list of resolved IP addresses.

    Parameters:
    targets (list of str): A list of strings, each representing a target. Targets can be file paths 
                           containing IP addresses, URLs, CIDR notations, IP ranges, or hostnames.

    Returns:
    list of str: A list of resolved IP addresses as strings.
    """
    ips = []
    for target in targets:
        try:
            # Handle if the target is a file containing a list of IPs
            with open(target, 'r') as file:
                ips.extend(file.readlines())
        except IOError:
            # Handle if the target is a URL
            if '://' in target:
                ips.append(target)
            # Handle if the target is a CIDR notation
            elif '/' in target:
                try:
                    network = ipaddress.ip_network(target.strip(), strict=False)
                    ips.extend([str(ip) for ip in network.hosts()])
                except ValueError:
                    print(f"❌ [-] Invalid CIDR notation: {target}")
            else:
                # Handle if the target is an IP address or range
                if is_ip_address(target):
                    ips.append(target)
                else:
                    def ip_range_explode(start_ip, end_ip):
                        """
                        Generates a list of IP addresses within a given range.

                        Parameters:
                        start_ip (str): The starting IP address of the range.
                        end_ip (str): The ending IP address of the range.

                        Returns:
                        list of str: A list of IP addresses within the specified range.
                        """
                        def ip_to_int(ip):
                            parts = list(map(int, ip.split('.')))
                            return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

                        def int_to_ip(ip_int):
                            return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"
                        
                        start_int = ip_to_int(start_ip)
                        end_int = ip_to_int(end_ip)
                        
                        ip_range = [int_to_ip(ip) for ip in range(start_int, end_int + 1)]
                        
                        return ip_range
                    

                    # Handle if the target is an IP range or a list of IPs
                    if '-' in target:
                        start_ip, end_ip = target.split('-')
                        ips.extend(ip_range_explode(start_ip, end_ip))
                    elif ',' in target:
                        ips.extend(target.split(','))
                    else:
                        ips.append(target)
    
    return ips

def check_connection(ip, port, timeout):
    """
    Check connectivity to a given IP address and port.

    This function attempts to create a socket connection to the specified IP address and port,
    using either IPv4 or IPv6 depending on the IP address format. It returns the socket if successful,
    or `None` if an exception occurs.

    Args:
        ip (str): The IP address to connect to.
        port (int): The port number to connect to.
        timeout (int): The connection timeout in seconds.

    Returns:
        socket.socket: The connected socket object or `None` if an exception occurs.
    """
    try:
        family = socket.AF_INET6 if ':' in ip else socket.AF_INET
        sock = socket.socket(family, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        return sock
    except Exception as e:
        return None

def ip_to_tuple(ip):
    """
    Convert an IP address to a numeric tuple.

    This function converts an IPv4 address from a string to a tuple of integers.

    Args:
        ip (str): The IP address as a string.

    Returns:
        tuple: A tuple containing the numeric representation of the IP address.
    """
    return tuple(map(int, ip.split('.')))

def is_ip_address(target):
    """
    Check if a string is a valid IP address.

    This function attempts to validate the given string as an IPv4 address.

    Args:
        target (str): The string to check.

    Returns:
        bool: `True` if the string is a valid IP address, `False` otherwise.
    """
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        return False
def process_ip_list(ip_list_file):
    """
    Process a file containing IP addresses or CIDR notations.

    This function reads IP addresses or CIDR notations from a file, expanding any CIDR notations
    into individual IP addresses. It returns a list of IP addresses.

    Args:
        ip_list_file (str): The path to the file containing IP addresses or CIDR notations.

    Returns:
        list: A list of IP addresses.
    """
    ips = []
    current_dir = os.getcwd()  # Get current working directory
    file_path = os.path.join(current_dir, ip_list_file)  # Build absolute path

    try:
        with open(file_path, 'r') as file:
            for target in file:
                target = target.strip()
                if '/' in target:
                    try:
                        network = ipaddress.ip_network(target, strict=False)
                        ips.extend([str(ip) for ip in network.hosts()])
                    except ValueError as e:
                        print(f"❌ [-] Invalid CIDR notation {target} {e}")
                else:
                    ips.append(target)
    except IOError:
        print(f"❌ [-] Could not read file: {file_path}")
        sys.exit()
    return [ip.strip() for ip in ips]

def get_banner(sock, timeout=1, limit_text=True):
    """
    Retrieve the HTTP or SSH banner from a socket connection.

    This function sends an HTTP GET request or handles an SSL/TLS connection if necessary,
    and retrieves the server's response. It returns the banner information, such as server details
    or any redirects.

    Args:
        sock (socket.socket): The socket object for the connection.
        timeout (int): The timeout for receiving data.
        limit_text (bool): Whether to limit the text length.

    Returns:
        str: The server banner or error message.
    """
    from app.utils.helper import get_tags_html, format_response

    try:
        sock.settimeout(timeout)

        ip, port = sock.getpeername()

        if port == 443:
            # Handle HTTPS connections
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=ip)

        # Send an HTTP GET request
        request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
        sock.sendall(request.encode())

        # Receive response
        response = b""
        while True:
            part = sock.recv(1024)
            if not part:
                break
            response += part

        response_str = response.decode(errors='ignore')
        
        headers = response_str.split("\r\n\r\n")[0].split("\r\n")

        title = get_tags_html(response_str) or ''
        if "301 Moved Permanently" in response_str:
            for line in response_str.split('\r\n'):
                if line.startswith('Location:'):
                    new_url = line[len('Location:'):].strip()
                    title = f"Redirect to: {new_url}"

        ssh_header = next((header.replace('\n', ' | ') for header in headers if header.startswith('SSH')), None)
        server_header = next(((title + ' ' + f"[{Colors.text(header, Colors.WHITE)}]") for header in headers if header.startswith('Server:')), None)
        
        return server_header or ssh_header or title or format_response(response_str, limit_text)
    except Exception as e:
        return Colors.text(str(e), Colors.RED)
    finally:
        sock.close()



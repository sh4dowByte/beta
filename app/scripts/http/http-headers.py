import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Disable InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

metadata = {
    'description': '''
        Get HTTP header
    ''',
    'author': 'sh4dowByte',
    'license': 'BETA',
    'portrule': ['http', 'https', 'proxmox'],
}

def run(ip, port, options):
    path = options.get('path', '/')
    useget = options.get('useget', False)

    if port == 443:
        url = f"https://{ip}:{port}{path}"
    else:
        url = f"http://{ip}:{port}{path}"

    try:
        # Tentukan jenis request (HEAD atau GET)
        if useget:
            response = requests.get(url, verify=False)
            request_type = "GET"
        else:
            response = requests.head(url, verify=False)
            request_type = "HEAD"

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve headers, status code: {response.status_code}")

        # Kembalikan hasil header
        headers = response.headers
        headers_output = "\n".join([f"{k}: {v}" for k, v in headers.items()])
        headers_output += f"\n(Request type: {request_type})"
        
        return headers_output
    except Exception as e:
        return f"[red]Error: {str(e)}[/red]"
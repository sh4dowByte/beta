import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# Disable InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

metadata = {
    'description': '''
        Get HTTP title
    ''',
    'author': 'sh4dowByte',
    'license': 'BETA',
    'portrule': ['http', 'https', 'proxmox'],
}

def run(ip, port, options):
    path = options.get('path', '/')

    if port == 443:
        url = f"https://{ip}:{port}{path}"
    else:
        url = f"http://{ip}:{port}{path}"

    try:
        # Tentukan jenis request (GET lebih tepat untuk mengambil title)
        response = requests.get(url, verify=False)
        request_type = "GET"

        if response.status_code != 200:
            raise Exception(f"[red]Failed to retrieve content, status code: {response.status_code}[/red]")

        # Parse HTML untuk mengambil title
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'

        # Kembalikan hasil title dan request type
        return f"Title: {title}\n(Request type: {request_type})"
    except Exception as e:
        return f"[red]Error: {str(e)}[/red]"

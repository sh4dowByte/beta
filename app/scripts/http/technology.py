import json
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

from app.utils.template import load_template, run_template

# Disable InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

metadata = {
    'description': '''
        Get Technology
    ''',
    'author': 'sh4dowByte',
    'license': 'BETA',
    'portrule': ['http', 'https'],
}

def run(ip, port, options):
    path = options.get('path', '/')

    templates, metadata_templates = load_template([])

   
    if port == 443:
        url = f"https://{ip}:{port}{path}"
    else:
        url = f"http://{ip}:{port}{path}"

    try:
        # Tentukan jenis request (GET lebih tepat untuk mengambil title)
        response = requests.get(url, verify=False)

        technology = []
        for template in templates:
            result = run_template(template['run'], response)

            if result is not None:
                for url, type, match_status, extracted_data, responses in result:
                    if match_status:
                        technology.append(template['run']['info']['name'])

        # Kembalikan hasil title dan request type
        return technology
    except Exception as e:
        return f"[red]Error: {str(e)}[/red]"
from urllib.parse import urlparse
import requests
import warnings
from app.utils.templates.matchers import *
from app.utils.templates.extractors import *
from urllib3.exceptions import InsecureRequestWarning
from rich.console import Console

# Disable InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

def match(config, response = '', ip = ''):
    """
    Perform dynamic HTTP requests based on the provided configuration.

    :param config: Configuration loaded from the YAML file
    :param base_url: Base URL of the target server
    :param timeout: Timeout for HTTP requests
    :return: Matching results or error messages
    """
    match_config = config.get('match', [])
    debug = config.get('debug', False)

    results = []

    for entry in match_config:
        stop_at_first_match = entry.get('stop-at-first-match', False)
        matchers_condition = entry.get('matchers-condition', 'and').lower()
        matchers = entry.get('matchers', [])
        extractors = entry.get('extractors', [])
        extract_separator = entry.get('extract-separator', ' | ')

        match_status = check_matchers(response, matchers, matchers_condition)
        extracted_data = apply_extractors(response, extractors, extract_separator)
        results.append((ip, match_status, extracted_data, response))
        if stop_at_first_match and match_status:
            break

    if debug and results:
        console = Console()
        console.log(results)

    return results

import re
import json
from bs4 import BeautifulSoup
from lxml import html

def apply_extractors(response, extractors, extract_separator=' | '):
    """
    Apply extractors to extract data from the HTTP response and merge results.

    :param response: HTTP response from the request
    :param extractors: List of extractors to apply
    :return: Merged extracted data as a single string separated by '|'
    """
    extracted_data = []
    first_separator = ''
    extract_separator = extract_separator.replace("\\n", "\n")
    extract_separator = extract_separator.replace("\\t", "\t")
    extract_separator = extract_separator.replace("\\r", "\r")

    if '\n' in extract_separator:
        first_separator = extract_separator

    for extractor in extractors:
        extractor_type = extractor.get('type')
        part = extractor.get('part', 'body')
        regex_patterns = extractor.get('regex', [])  # Regex patterns for regex extractor
        json_path = extractor.get('json_path', '')  # Path untuk JSON
        selector = extractor.get('selector', '')  # XPath, CSS Selector, atau tag HTML
        group = extractor.get('group', 0)  # Group untuk regex extractor

        show = False
        if extractor_type == 'regex':
            if part == 'body':
                for pattern in regex_patterns:
                    if '{' in pattern and '}' in pattern:
                        extracted_value = pattern
                        for placeholder in re.findall(r'\{(.*?)\}', pattern):
                            match = re.search(placeholder, response.text)
                            if match:
                                show = True
                                extracted_value = extracted_value.replace(f'{{{placeholder}}}', match.group(group))
                        if show:
                            extracted_data.append(extracted_value)
                    else:
                        match = re.search(pattern, response.text)
                        if match:
                            extracted_data.append(match.group(group))
            elif part == 'header':
                for pattern in regex_patterns:
                    for key in response.headers:
                        if '{' in pattern and '}' in pattern:
                            extracted_value = pattern
                            for placeholder in re.findall(r'\{(.*?)\}', pattern):
                                match = re.search(placeholder, response.headers.get(key, ''))
                                if match:
                                    show = True
                                    extracted_value = extracted_value.replace(f'{{{placeholder}}}', match.group(group))
                            if show:
                                extracted_data.append(extracted_value)
                        else:
                            match = re.search(pattern, response.headers.get(key, ''))
                            if match:
                                extracted_data.append(match.group(group))

        elif extractor_type == 'json':
            try:
                json_data = json.loads(response.text)
                if '{' in json_path and '}' in json_path:
                    extracted_value = json_path
                    for placeholder in re.findall(r'\{(.*?)\}', json_path):
                        value = json_data
                        for key in placeholder.split('.'):
                            if isinstance(value, list):
                                key = int(key)
                            value = value[key]
                        extracted_value = extracted_value.replace(f'{{{placeholder}}}', str(value))
                    extracted_data.append(extracted_value)
                    if show:
                        extracted_data.append(extracted_value)
                else:
                    value = json_data
                    for key in json_path.split('.'):
                        if isinstance(value, list):
                            key = int(key)
                        value = value[key]
                    extracted_data.append(str(value))
            except (json.JSONDecodeError, KeyError, IndexError, ValueError) as e:
                print(f"Error extracting JSON data: {e}")

        elif extractor_type == 'xpath':
            try:
                tree = html.fromstring(response.text)
                if '{' in selector and '}' in selector:
                    extracted_value = selector
                    for placeholder in re.findall(r'\{(.*?)\}', selector):
                        selected_elements = tree.xpath(placeholder)
                        value = selected_elements[0].text_content().strip() if selected_elements else ''
                        extracted_value = extracted_value.replace(f'{{{placeholder}}}', value)
                    extracted_data.append(extracted_value)
                else:
                    selected_elements = tree.xpath(selector)
                    for element in selected_elements:
                        text_content = element.text_content().strip()
                        extracted_data.append(text_content)
            except Exception as e:
                print(f"Error extracting HTML data: {e}")

        elif extractor_type == 'html':
            try:
                # Parsing HTML dari response body
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Jika selector mengandung '{}', proses placeholder-nya
                if '{' in selector and '}' in selector:
                    extracted_value = selector
                    for placeholder in re.findall(r'\{(.*?)\}', selector):
                        selected_elements = soup.select(placeholder)
                        value = selected_elements[0].get_text().strip() if selected_elements else ''
                        extracted_value = extracted_value.replace(f'{{{placeholder}}}', value)
                    extracted_data.append(extracted_value)
                else:
                    # Mengambil nilai berdasarkan CSS selector yang diberikan
                    selected_elements = soup.select(selector)
                    for element in selected_elements:
                        text_content = element.get_text().strip()
                        extracted_data.append(text_content)
            except Exception as e:
                print(f"Error extracting HTML data: {e}")
    
    if extracted_data:
        return first_separator + extract_separator.join(extracted_data)

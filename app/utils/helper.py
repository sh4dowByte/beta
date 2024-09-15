from app.config import App
from app.utils.style import Colors, TextFormat
import re

def display_banner():
    """
    Display a banner with a version number and random text.

    This function prints a stylized banner including a version number and a randomly chosen text
    in different colors.

    Returns:
        None
    """
    banner = rf"""
    {Colors.GREEN}
        ____       __       
       / __ )___  / /_____ _
      / __  / _ \/ __/ __ `/
     / /_/ /  __/ /_/ /_/ / 
    /_____/\___/\__/\__,_/     v{App.version}
    {Colors.RESET}
                      {TextFormat.text('Port Scanner')}
    
    """
    print(banner)

def get_tags_html(html, tags='title'):
    """
    Extract the content of a specified HTML tag from a string.

    This function uses a regular expression to find the content between the specified HTML tags.

    Args:
        html (str): The HTML string to search.
        tags (str): The tag to search for.

    Returns:
        str: The content within the specified tags or `None` if the tag is not found.
    """
    pattern = rf'<{tags}>(.*?)</{tags}>'
    match = re.search(pattern, html, re.IGNORECASE)

    if match:
        return match.group(1).strip()
    else:
        return None

def format_response(response_str, limit_text=True):
    """
    Format the HTTP response string for display.

    This function trims the response string to a specified length if `limit_text` is `True`,
    and removes excess whitespace.

    Args:
        response_str (str): The HTTP response string.
        limit_text (bool): Whether to limit the text length.

    Returns:
        str: The formatted response string.
    """
    if not limit_text:
        return response_str
    
    limit_str = 100
    response_str = ' '.join(response_str.split())
    return response_str[:limit_str] + '...' if len(response_str) > limit_str else response_str

def tabbed_result(text, tab_size = 2, line = ''):
    """
    Add indentation to the text for better readability.

    Args:
        text (str): The text to format.

    Returns:
        str: The formatted text.
    """
    tab = ' ' * tab_size
    lines = text.split('\n')
    formatted_lines = [lines[0]] + [tab + line for line in lines[1:]]
    return f"\n{line}".join(formatted_lines)

def print_result(msg, ip = None):
    """
    Prints the result of a scan with formatted output including IP, and a message.

    Parameters:
    ip (str): The IP address to be printed (can be None).
    msg (str): The message to be printed.
    """
    if ip:
        ip = f"[{Colors.text(f"{ip}")}] "
    else:
        ip = ''

    text = (f"Server on {ip}"
          f" "
          f"{msg}")
    
    print(text+'\n')

    # Menghapus kode warna dari string
    clean_text = re.compile(r'\x1B\[([0-9]{1,2}(?:;[0-9]{1,2})*)m').sub('', text)

    return clean_text


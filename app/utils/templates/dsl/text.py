import random
import string


def contains(text, substring):
    """
    Memeriksa apakah substring ada di dalam text.
    
    :param text: Teks yang akan diperiksa.
    :param substring: Substring yang dicari.
    :return: True jika substring ditemukan, False sebaliknya.
    """
    return substring in text

def to_lower(text):
    return text.lower()

def rand_base(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

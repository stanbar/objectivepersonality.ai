import re
import unicodedata

def normalize_name(name: str) -> str:
    # Step 1: Normalize and remove diacritics using unicodedata
    normalized = unicodedata.normalize('NFKD', name)
    result = ''.join(c for c in normalized if not unicodedata.combining(c))
    # Step 2: Replace whitespace with _
    result = re.sub(r'\s', '_', result)
    # Step 3: Remove quotes, parentheses, and hyphens
    result = re.sub(r"[\'\"()\-]", '', result)
    # Step 4: Replace & with _, . with _, and both / and \ with _
    result = re.sub(r'&', '_', result)
    result = re.sub(r'\.', '_', result)
    result = re.sub(r'[\\/]', '_', result)
    # Step 5: Consolidate multiple _ into a single _ and trim any leading/trailing _
    result = re.sub(r'_+', '_', result)
    result = result.strip('_')
    return result
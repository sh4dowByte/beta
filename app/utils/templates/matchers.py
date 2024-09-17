import re
from app.utils.templates.dsl import *

def check_matchers(response, matchers, matchers_condition):
    """
    Check response matching based on the provided matchers.

    :param response: response from the request
    :param matchers: List of matchers to check
    :param matchers_condition: Matching condition ('and' or 'or')
    :return: Matching status
    """
    results = []


    status_code = response.status_code  # Default to 0 if status_code is None

    headers = response.headers or {}  # Default to an empty dictionary if headers is None
    body = response.text or ""  # Default to an empty string if body is None

    for matcher in matchers:
        matcher_type = matcher.get('type')
        part = matcher.get('part', 'body')
        condition = matcher.get('condition', 'or').lower()
        matcher_words = matcher.get('words', [])
        regex = matcher.get('regex', [])

        if matcher_type == 'status':
            results.append(status_code in matcher.get('status', []))
            continue
        elif matcher_type == 'word':
            if part == 'header':
                header_words = [word for word in matcher_words if any(word in headers.get(key, '') for key in headers)]
                if condition == 'and':
                    results.append(all(word in header_words for word in matcher_words))
                elif condition == 'or':
                    results.append(any(word in header_words for word in matcher_words))
            elif part == 'body' or part is None:
                if condition == 'and':
                    results.append(all(word in body for word in matcher_words))
                elif condition == 'or':
                    results.append(any(word in body for word in matcher_words))
        elif matcher_type == 'regex':
            if part == 'body':
                for pattern in regex:
                    if re.search(pattern, body):
                        results.append(True)
                    else:
                        results.append(False)
            elif part == 'header':
                for pattern in regex:
                    if any(re.search(pattern, headers.get(key, '')) for key in headers):
                        results.append(True)
                    else:
                        results.append(False)
        elif matcher_type == 'dsl':
            for dsl_expression in matcher.get('dsl', []):
                try:
                    if eval(dsl_expression, dsl_context, {"response": response}):
                        results.append(True)
                    else:
                        results.append(False)
                except Exception as e:
                    print(f"Error evaluating DSL expression '{dsl_expression}': {e}")
                    results.append(False)

    if matchers_condition == 'and':
        return all(results)
    elif matchers_condition == 'or':
        return any(results)
    else:
        raise ValueError(f"Unsupported matchers-condition: {matchers_condition}")

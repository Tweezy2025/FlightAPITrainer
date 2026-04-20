import requests
import json

def make_request(method, base_url, endpoint, payload=None, headers=None):
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    response = requests.request(
        method=method,
        url=url,
        json=payload,
        headers=headers or {"Content-Type": "application/json"}
    )
    return response

def validate_json_response(response):
    try:
        response.json()
        return True
    except json.JSONDecodeError:
        return False

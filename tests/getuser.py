#!/usr/bin/env python
"""Unittest for main API endpoint."""
import sys
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("stanleyjobson", "swordfish")
response = requests.get(
     "http://localhost:8000/users/me",
     timeout=5,
     auth=auth,
)
if response.status_code != 200:
    status_code = response.status_code
    detail = response.json()["detail"]
    print(f"Error {status_code}: {detail}")
    sys.exit(1)
print(response.json())
sys.exit(0)

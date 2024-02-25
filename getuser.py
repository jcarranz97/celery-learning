import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("stanleyjobson", "swordfish")
response = requests.get("http://localhost:8000/users/me", auth=auth)
if response.status_code == 200:
    print(response.json())
else:
    status_code = response.status_code
    detail = response.json()["detail"]
    print(f"Error {status_code}: {detail}")

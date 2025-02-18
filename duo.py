import requests

# Create a session to maintain cookies
session = requests.Session()

# Define the login URL
login_url = "https://fr.duolingo.com/log-in?isLoggingIn=true"

# Your credentials (replace with actual values)
payload = {
    "identifier": "OlivierGilbert24",
    "password": "your_password"
}

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

# Send the login request
response = session.post(login_url, json=payload, headers=headers)

# Check if login was successful
if response.status_code == 200:
    print("Login successful!")
    print("Status Code:", response.status_code)
    #print("Response Text:", response.text)
    with open('out.html', 'w', encoding="utf-8") as f:
        f.write(response.text)

    #print("Response:", response.json())  # The response contains user details and session info
else:
    print("Login failed:", response.text)

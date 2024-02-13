import requests
import json

def request_completion(prompt, max_tokens=50):
    url = "https://your_gpt_api_endpoint.com/completion"  # Replace this with your API endpoint
    headers = {
        "Content-Type": "application/json",
        "application-name": application_name,
        "key-name": key_name,
        "key-value": key_value
    }
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print("Error:", response.text)
        return None

def read_github_file(repo_url, file_path):
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + "/main/" + file_path
    response = requests.get(raw_url)
    if response.status_code == 200:
        return response.text
    else:
        print("Error:", response.text)
        return None

# Set up your API credentials
application_name = "your_application_name"
key_name = "your_key_name"
key_value = "your_key_value"

# Specify GitHub repository URL and file path
repo_url = "https://github.com/your_username/your_repository"
file_path = "path/to/your/file.txt"

# Read file from GitHub repository
file_content = read_github_file(repo_url, file_path)
if file_content:
    prompt = "Please summarize the contents of the file:\n" + file_content
    completion = request_completion(prompt)
    if completion:
        print("Generated summary:", completion["choices"][0]["text"].strip())

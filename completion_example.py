import requests
import json

prompts = [
        """\
import socket

def ping_exponential_backoff(host: str):""",
        """\
import argparse

def main(string: str):
    print(string)
    print(string[::-1])

if __name__ == "__main__":"""
]


def send_request(input_str):
    url = 'http://127.0.0.1:/v1/completion'
    headers = {'Content-Type': 'application/json'}
    data = {'input': input_str}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return f'Error: {response.status_code}'

if __name__ == '__main__':
    for prompt in prompts:
        result = send_request(prompt)
        print(result)


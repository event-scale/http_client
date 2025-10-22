import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from http_client import Http


def test_http_client():
    def retry_callback(attempt: int, e):
        print(f"Attempt {attempt} failed with error {e}")
        time.sleep(attempt * 1.1)

    Http().retry(3, retry_callback).get("http://127.0.0.1:7000")

def test_http_client_with_post():
    Http().post('http://127.0.0.1:7000', {
        'name': 'Bedram',
        'email': 'tmgbedu@gmail.com'
    })

def test_http_client_with_post_as_form():
    Http().asForm().post('http://127.0.0.1:7000', {
        'name': 'Bedram',
        'email': 'tmgbedu@gmail.com'
    })

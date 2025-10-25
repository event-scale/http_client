import os
import sys

import responses

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from http_client import Http

URL = "http://127.0.0.1:7000/"


@responses.activate
def test_http_client_with_get():
    responses.add(responses.GET, URL, status=200, json={"ok": True})

    response = Http().get('http://127.0.0.1:7000', {
        'name': 'Alex',
    })

    assert response.status_code == 200
    assert len(responses.calls) == 1
    request = responses.calls[0].request
    assert request.url == "http://127.0.0.1:7000/?name=Alex"


@responses.activate
def test_http_client_with_post():
    responses.add(responses.POST, URL, status=200, json={"ok": True})

    response = Http().post('http://127.0.0.1:7000', {
        'name': 'Bedram',
        'email': 'tmgbedu@gmail.com'
    })

    assert response.status_code == 200


@responses.activate
def test_http_client_with_post_as_form():
    responses.add(responses.POST, URL, status=200, json={"ok": True})

    Http().asForm().post('http://127.0.0.1:7000', {
        'name': 'Bedram',
        'email': 'tmgbedu@gmail.com'
    })

    assert len(responses.calls) == 1
    request = responses.calls[0].request

    assert request.headers["Content-Type"] == "application/x-www-form-urlencoded"
    assert request.body == "name=Bedram&email=tmgbedu%40gmail.com"


@responses.activate
def test_http_client():
    responses.add(responses.GET, URL, status=500)
    responses.add(responses.GET, URL, status=200, json={"ok": True})

    failed_callback = False

    def retry_callback(attempt: int, e):
        nonlocal failed_callback
        print(f"Attempt {attempt} failed with error {e}")
        failed_callback = True

    Http().retry(3, retry_callback).get(URL)
    assert failed_callback == True

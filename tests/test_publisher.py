#!/usr/bin/env python3

import pytest

import sys
sys.path.append('.')

from publisher import publish
from flask import Flask, current_app

app = Flask(__name__)


@pytest.fixture()
def create_test_app():
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(create_test_app):
    return app.test_client()


@app.route("/auto_main", methods=["POST"])
@publish()
def auto_main(arg):
    current_app.test_args = (arg,)
    return "ok"


def test_auto_main(client):
    response = client.post("/auto_main", data={"arg": "footest"})
    assert response.status_code == 200
    assert b"ok" in response.data
    assert app.test_args == ("footest",)


@app.route("/auto_args_and_kw", methods=["POST"])
@publish()
def auto_args_and_kw(arg, opt):
    current_app.test_args = (arg, opt)
    return "ok"


def test_auto_args_and_kw(client):
    response = client.post("/auto_args_and_kw", data={"arg": "footest", "opt": "fooopt"})
    assert response.status_code == 200
    assert b"ok" in response.data
    assert app.test_args == ("footest", "fooopt")


@app.route("/auto_dynamic", methods=["POST"])
@publish()
def auto_dynamic(arg, opt, **kw):
    current_app.test_args = (arg, opt, kw["dynamic"])
    return "ok"


def test_auto_dynamic(client):
    response = client.post(
        "/auto_dynamic", data={"arg": "footest", "opt": "fooopt", "dynamic": "dynarg"}
    )
    assert response.status_code == 200
    assert b"ok" in response.data
    assert app.test_args == ("footest", "fooopt", "dynarg")


@app.route("/auto_hello", methods=["POST"])
@publish()
def auto_hello(age:int, message='Hello', name:str='world'):
    assert type(age) is int
    return f'{message} {name} you are {age}'


def test_auto_hello(client):
    response = client.post(
        "/auto_hello", data={'age': '12'}
    )
    assert response.status_code == 200
    assert b"Hello world you are 12" in response.data

    response = client.post(
        "/auto_hello", data={'name': 'Sean', 'message': 'Hola', 'age': '50'}
    )
    assert response.status_code == 200
    assert b"Hola Sean you are 50" in response.data

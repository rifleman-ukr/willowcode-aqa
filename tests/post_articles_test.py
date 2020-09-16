import random
import uuid

import pytest


def test_create_article(send_request):
    response = send_request(method='POST',
                       payload={"title": (title := str(uuid.uuid4())),
                                "text": (text := str(uuid.uuid4()))})
    assert response.status_code == 200
    assert response.json() == {"title": title.capitalize(), "text": text}
    return response.json()


def test_update_article(send_request):
    article = test_create_article(send_request)
    response = send_request(method='POST',
                            payload={"title": article['title'],
                                     "text": (text := str(uuid.uuid4()))})
    assert response.status_code == 200
    assert response.json() == {"title": article['title'], "text": text}


def test_update_with_same_text(send_request):
    article = test_create_article(send_request)
    response = send_request(method='POST',
                            payload={"title": article['title'],
                                     "text": article['text']})
    assert response.status_code == 200
    assert response.json() == {"error": "This text is outdated"}


@pytest.mark.parametrize("title", (random.seed(),
                                   {1: True},
                                   [],
                                   random.choice([True, False]),
                                   None))
def test_create_article_with_wrong_title(send_request, title):
    response = send_request(method='POST',
                            payload={"title": title,
                                     "text": str(uuid.uuid4())})
    assert response.status_code == 415


def test_set_article_version(send_request):
    article = test_create_article(send_request)
    response = send_request(method='POST',
                            endpoint='/version_set',
                            payload={"title": article['title'].capitalize(),
                                     "version": 0},
                            headers={'Authorization': 'admin'})
    assert response.status_code == 200
    assert response.json() == {"text": "An empty article",
                               "title": article['title']}


@pytest.mark.parametrize("version", (str(uuid.uuid4()),
                                     {1: True},
                                     [],
                                     random.choice([True, False]),
                                     None))
def test_set_wrong_article_version(send_request, version):
    article = test_create_article(send_request)
    response = send_request(method='POST',
                            endpoint='/version_set',
                            payload={"title": article['title'].capitalize(),
                                     "version": version},
                            headers={'Authorization': 'admin'})
    assert response.status_code == 415


def test_set_article_version_no_auth(send_request):
    article = test_create_article(send_request)
    response = send_request(method='POST',
                            endpoint='/version_set',
                            payload={"title": article['title'].capitalize(),
                                     "version": 0})
    assert response.status_code == 401

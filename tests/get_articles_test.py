def test_get_all_articles(send_request):
    assert (response := send_request()).status_code == 200
    assert isinstance(response.json(), list)


def test_get_random_article(send_request):
    assert (response := send_request(endpoint='/random')).status_code == 200
    assert isinstance(response.json(), dict)


def test_delete_request(send_request):
    assert send_request(method='DELETE').status_code == 405

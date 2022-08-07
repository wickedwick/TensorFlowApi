from unittest.mock import Mock

from fastapi.testclient import TestClient

from image_classification import classifier
from main import app


def test_read_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_post_classify(monkeypatch):
    my_mock = Mock()
    monkeypatch.setattr(
        'image_classification.classifier.run_inference_on_image', my_mock)

    client = TestClient(app)
    response = client.post(
        "/classify", json={"image": "TWFueSBoYW5kcyBtYWtlIGxpZ2h0IHdvcmsu", "num_top_predictions": 5})

    print(response.json())
    assert response.status_code == 200
    assert my_mock.called
    assert response.json() == {"class": "Google"}

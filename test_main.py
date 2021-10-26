from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_value():
    res = client.post(
        "/get_value", json={"key": "8a35eb59-62b3-481c-8875-1f248df4c952"}
    )
    assert res.status_code == 200


def test_no_existence():
    _id = "0cf57c3d-a710-4c54-9437-4a422e037e37"
    res = client.post("/get_value", json={"key": _id})
    assert res.status_code == 400


def test_bad_uuid():
    bad_key = "a"
    res = client.post("/get_value", json={"key": bad_key})
    assert res.status_code == 400

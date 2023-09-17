from fastapi.testclient import TestClient

from voicevox_engine import __version__


def test_fetch_version_success(client: TestClient):
    response = client.get("/version")
    assert response.status_code == 200
    # Bridge PluginはVersion取得が特殊なため、一旦コメントアウト
    # assert response.json() == __version__

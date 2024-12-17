import requests
from core import settings

def register_apis_to_gatekeeper():

    # Login
    at = requests.post(
        url=settings.GATEKEEPER_BASE_URL.unicode_string() + "api/login/",
        headers={"Content-Type": "application/json"},
        json={"username": "admin", "password": "admin"}
    )

    temp = at.json()

    access = temp["access"]
    refresh = temp["refresh"]

    # Register APIs
    # APIs shouldn't have slashes on their ends even though they do have them
    apis_to_register = [
        ("api/v1/data/upload", ["POST"], "pdm"), ("api/v1/pest-model",["POST", "GET"], "pdm"),
        ("api/v1/rule", ["GET", "POST", "DELETE"], "pdm"),
        ("api/v1/tool/calculate-risk-index/weather/{weather_dataset_id}/model/{model_ids}/verbose", ["GET"], "pdm"),
        ("api/v1/tool/calculate-risk-index/weather/{weather_dataset_id}/model/{model_ids}/high", ["GET"], "pdm")
    ]

    for atr in apis_to_register:
        requests.post(
            url=settings.GATEKEEPER_BASE_URL.unicode_string() + "api/register_service/",
            headers={"Content-Type": "application/json", "Authorization" : "Bearer {}".format(access)},
            json={
                "base_url": "pdm_backend:8003",
                "service_name": atr[2],
                "endpoint": atr[0],
                "methods": atr[1]
            }
        )

    # Logout
    requests.post(
        url=settings.GATEKEEPER_BASE_URL.unicode_string() + "api/logout/",
        headers={"Content-Type": "application/json"},
        json={"refresh": refresh}
    )

    return

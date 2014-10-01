import requests


def fetch_kml_document(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

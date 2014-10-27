import fastkml
import lxml
import requests


def fetch_kml_document(url):

    candidates = (url, url + '/@@kml-document')

    for url in candidates:
        response = requests.get(url)

        if response.status_code != 200:
            continue

        try:
            fastkml.kml.KML().from_string(response.content)
        except (lxml.etree.XMLSyntaxError, TypeError):
            continue
        else:
            return response.content

    return None

import requests

BASE_URL_WES='http://127.0.0.1:5001/'
BASE_URL_DJANGO='http://127.0.0.1:5000/'

class TestHTML:

    def test_html_matches(self):
        wes_html = requests.get(BASE_URL_WES)
        dfsdjango_html = requests.get(BASE_URL_DJANGO)
        assert wes_html.text == dfsdjango_html.text

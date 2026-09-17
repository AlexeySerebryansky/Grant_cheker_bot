import requests

class Client:

    def get_html(self, url: str) -> str:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        return response.text
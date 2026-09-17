from pathlib import Path

from parser.client import Client
from parser.parser import Parser
from parser.storage import Storage
from parser.comparator import Comparator

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_FILE = BASE_DIR / "storage.json"

def test():
    client = Client()
    parser = Parser()
    storage = Storage(STORAGE_FILE)
    comparator = Comparator()

    url = "https://grant-av.com.ua/grants/"
    html = client.get_html(url)

    new_data = parser.parse(html)
    old_data = storage.load()

    changes = comparator.compare(old_data, new_data)

    print("ADDED:", changes["added"])
    print("REMOVED:", changes["removed"])
    print("UPDATED:", changes["updated"])

    storage.save(new_data)

if __name__ == "__main__":
    test()
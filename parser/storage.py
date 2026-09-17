import json

class Storage:

    def __init__(self, path: str):
        self.path = path

    def load(self) -> dict:
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self, data: dict) -> None:
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )
import json
import os

class Localization:
    def __init__(self, lang="en"):
        locales_dir = os.path.join(os.path.dirname(__file__), "..", "locales")
        path = os.path.join(locales_dir, f"{lang}.json")
        with open(path, "r", encoding="utf-8") as f:
            self.messages = json.load(f)

    def t(self, key, **kwargs):
        # Підтримка вкладених ключів "deck.enter"
        parts = key.split(".")
        msg = self.messages
        for part in parts:
            msg = msg.get(part, {})
        if not isinstance(msg, str):
            return key  # Якщо ключ не знайдено
        return msg.format(**kwargs)

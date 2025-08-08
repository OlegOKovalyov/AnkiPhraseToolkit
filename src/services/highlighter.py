# src/services/highlighter.py
class Highlighter:
    def highlight(self, sentence: str, expression: str) -> str:
        return sentence.replace(expression, f"<b>{expression}</b>")

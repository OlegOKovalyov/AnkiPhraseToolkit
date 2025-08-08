# src/models/sentence.py
from .expression import Expression

class Sentence:
    def __init__(self, text: str, expression: Expression):
        self.text = text
        self.expression = expression
        self.highlighted: Optional[str] = None

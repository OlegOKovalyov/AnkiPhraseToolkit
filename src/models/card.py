# src/models/card.py
from .expression import Expression
from .sentence import Sentence

class AnkiCard:
    def __init__(self, expression: Expression, sentence: Sentence):
        self.expression = expression
        self.sentence = sentence
        self.audio_expression_path: Optional[str] = None
        self.audio_sentence_path: Optional[str] = None

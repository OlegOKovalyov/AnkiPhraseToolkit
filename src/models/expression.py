# src/models/expression.py
from typing import List, Optional

class Expression:
    def __init__(self, text: str):
        self.text = text
        self.meaning: Optional[str] = None
        self.translation: Optional[str] = None
        self.examples: List[str] = []


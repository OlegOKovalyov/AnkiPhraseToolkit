# src/services/expression_detector.py
class ExpressionDetector:
    def detect(self, sentence: str, expression: str) -> bool:
        return expression.lower() in sentence.lower()

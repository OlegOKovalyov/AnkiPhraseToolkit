# main.py
from src.models.expression import Expression
from src.models.sentence import Sentence
from src.models.card import AnkiCard
from src.services.highlighter import Highlighter
from src.services.expression_detector import ExpressionDetector
from src.services.definition_fetcher import DefinitionFetcher
from src.services.example_fetcher import ExampleFetcher
from src.services.tts_generator import TTSGenerator
from src.export.anki_exporter import AnkiExporter

# Демонстрація базового використання
if __name__ == "__main__":
    expression = Expression("get rid of")
    sentence = Sentence("I need to get rid of these old clothes.", expression)

    detector = ExpressionDetector()
    if not detector.detect(sentence.text, expression.text):
        print("Expression not found in sentence!")
        exit()

    highlighter = Highlighter()
    sentence.highlighted = highlighter.highlight(sentence.text, expression.text)

    definition_fetcher = DefinitionFetcher()
    expression.meaning = definition_fetcher.fetch(expression.text)

    example_fetcher = ExampleFetcher()
    expression.examples = example_fetcher.fetch(expression.text)

    expression.translation = "позбутися"

    tts = TTSGenerator()
    tts.generate(expression.text, "audio/expression.mp3")
    tts.generate(sentence.text, "audio/sentence.mp3")

    card = AnkiCard(expression, sentence)
    card.audio_expression_path = "audio/expression.mp3"
    card.audio_sentence_path = "audio/sentence.mp3"

    exporter = AnkiExporter()
    exporter.export([card], "anki_cards.tsv")

    print("Card exported.")

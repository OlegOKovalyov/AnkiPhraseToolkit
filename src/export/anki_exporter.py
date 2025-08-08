# src/export/anki_exporter.py
import csv
from typing import List
from src.models.card import AnkiCard

class AnkiExporter:
    def export(self, cards: List[AnkiCard], file_path: str) -> None:
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            for card in cards:
                writer.writerow([
                    card.expression.text,
                    card.expression.meaning,
                    card.sentence.text,
                    card.audio_sentence_path or '',
                    card.audio_expression_path or '',
                    '; '.join(card.expression.examples),
                    card.expression.translation or ''
                ])

# src/cli/cli.py
import argparse

class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="AnkiPhraseToolkit CLI - Phrase-Based Learning Assistant"
        )
        self.parser.add_argument("--user", type=str, help="Username for the session")
        self.parser.add_argument("--lang", type=str, default="en", help="Interface language")

    def parse_args(self):
        return self.parser.parse_args()

# src/cli/cli.py
import argparse
import sys
from typing import Optional


class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="AnkiPhraseToolkit v0.1 CLI for Phrase-Based Learning Assistant"
        )
        self.parser.add_argument(
            "--user", 
            type=str, 
            help="Username for the session (will override current user if provided)"
        )
        self.parser.add_argument(
            "--lang", 
            type=str, 
            default="en", 
            help="Interface language"
        )

    def parse_args(self):
        # Parse without exiting on unknown to provide a quiet, custom error message
        args, unknown = self.parser.parse_known_args()
        if unknown:
            print("❌ Error: unrecognized or invalid arguments.")
            print('💡 Usage: python3 -m src.main --user "User Name"\nExiting...')
            sys.exit(1)
        return args
    
    def get_user_argument(self) -> Optional[str]:
        """Get the user argument from parsed args."""
        args = self.parse_args()
        return args.user

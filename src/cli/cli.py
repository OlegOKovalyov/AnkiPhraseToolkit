# src/cli/cli.py
import argparse
import sys
from typing import Optional

from src.utils.localization import Localization
from src.utils.notifier import Notifier


class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="AnkiPhraseToolkit CLI"
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
        lang = getattr(args, "lang", "en")
        loc = Localization(lang=lang)
        notifier = Notifier()
        if unknown:
            notifier.error(loc.t("cli.invalid_args"))
            notifier.info(loc.t("cli.usage"))
            sys.exit(1)
        return args
    
    def get_user_argument(self) -> Optional[str]:
        """Get the user argument from parsed args."""
        args = self.parse_args()
        return args.user

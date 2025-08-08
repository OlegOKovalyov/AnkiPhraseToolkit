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
        try:
            args = self.parser.parse_args()
            self._check_username_format(args.user)
            return args
        except SystemExit:
            # Handle the case where argparse exits due to unrecognized arguments
            print("❌ Error: Username with spaces must be enclosed in quotes!")
            print("💡 Correct usage: python3 -m src.main --user \"User 1\"")
            print("📝 Example: python3 -m src.main --user \"User Name\"")
            print()
            # Return a default args object to continue execution
            return argparse.Namespace(user=None, lang="en")
    
    def _check_username_format(self, username: Optional[str]) -> None:
        """Check if username contains spaces and warn about proper quoting."""
        if username and ' ' in username:
            print("⚠️  Warning: Username contains spaces!")
            print("💡 For usernames with spaces, use quotes: --user \"User Name\"")
            print("📝 Example: python3 -m src.main --user \"User 1\"")
            print()
    
    def get_user_argument(self) -> Optional[str]:
        """Get the user argument from parsed args."""
        args = self.parse_args()
        return args.user

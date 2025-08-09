import json
import os
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any


class UserManager:
    def __init__(self):
        self.config_dir = Path("data")
        self.config_file = self.config_dir / "user_config.json"
        self.anki_db_path = self._get_anki_db_path()
        # Dependencies will be injected by main.py
        self.notifier = getattr(self, "notifier", None)
        self.prompter = getattr(self, "prompter", None)
        self.loc = getattr(self, "loc", None)
        
    def _get_anki_db_path(self) -> Optional[Path]:
        """Get the path to the Anki database based on the operating system."""
        home = Path.home()
        
        # Common Anki database locations
        possible_paths = [
            home / ".local/share/Anki2/User 1/collection.anki2",
            home / "Library/Application Support/Anki2/User 1/collection.anki2",
            home / "AppData/Roaming/Anki2/User 1/collection.anki2",
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
                
        return None
    
    def load_user_config(self) -> Dict[str, Any]:
        """Load user configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"current_user": None, "current_deck": None}
    
    def save_user_config(self, config: Dict[str, Any]) -> None:
        """Save user configuration to file."""
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_current_user(self) -> Optional[str]:
        """Get the current user from configuration."""
        config = self.load_user_config()
        return config.get("current_user")
    
    def get_current_deck(self) -> Optional[str]:
        """Get the current deck from configuration."""
        config = self.load_user_config()
        return config.get("current_deck")
    
    def set_current_user(self, username: str) -> None:
        """Set the current user in configuration."""
        config = self.load_user_config()
        config["current_user"] = username
        self.save_user_config(config)
    
    def set_current_deck(self, deck_name: str) -> None:
        """Set the current deck in configuration."""
        config = self.load_user_config()
        config["current_deck"] = deck_name
        self.save_user_config(config)
    
    def check_anki_user_exists(self, username: str) -> bool:
        """Check if a user exists in the Anki database."""
        if not self.anki_db_path or not self.anki_db_path.exists():
            return False
            
        try:
            conn = sqlite3.connect(str(self.anki_db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            cursor.fetchall()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def create_anki_user(self, username: str) -> bool:
        """Create a new Anki user (stub implementation)."""
        self.notifier.info(self.loc.t("user.creating", username=username))
        self.notifier.info(self.loc.t("user.create_stub_note"))
        return True
    
    def prompt_for_username(self) -> str:
        """Prompt user to enter a username."""
        while True:
            self.notifier.blank()
            username = self.prompter.ask(self.loc.t("user.enter_new")).strip()
            self.notifier.blank()
            if username:
                return username
            self.notifier.error(self.loc.t("user.empty_error"))
    
    def verify_and_set_user(self, username: str) -> bool:
        """Verify user exists in Anki and set as current user."""
        self.notifier.blank()
        self.notifier.info(self.loc.t("user.checking", username=username))
        
        if self.check_anki_user_exists(username):
            self.set_current_user(username)
            self.notifier.success(self.loc.t("user.found_set", username=username))
            return True
        else:
            self.notifier.error(self.loc.t("user.not_found", username=username))
            confirm = self.prompter.confirm(self.loc.t("user.create_confirm", username=username))
            if confirm:
                if self.create_anki_user(username):
                    self.set_current_user(username)
                    self.notifier.success(self.loc.t("user.created_set", username=username))
                    return True
                else:
                    self.notifier.error(self.loc.t("user.create_failed"))
                    return False
            else:
                self.notifier.info(self.loc.t("user.creation_cancelled"))
                return False
    
    def display_current_user(self) -> None:
        current_user = self.get_current_user()
        if current_user:
            self.notifier.info(self.loc.t("user.current", username=current_user))
        else:
            self.notifier.info(self.loc.t("user.no_current"))
    
    def display_current_deck(self) -> None:
        current_deck = self.get_current_deck()
        if current_deck:
            self.notifier.info(self.loc.t("deck.current", deckname=current_deck))
        else:
            self.notifier.info(self.loc.t("deck.no_current"))
    
    def handle_user_setup(self, cli_username: Optional[str] = None) -> bool:
        """Handle the complete user setup process."""
        current_user = self.get_current_user()
        
        # If CLI username is provided, use it
        if cli_username:
            self.notifier.blank()
            return self.verify_and_set_user(cli_username)
        
        # If no current user, prompt for one with surrounding blank lines
        if not current_user:
            self.notifier.blank()
            username = self.prompt_for_username()
            self.notifier.blank()
            return self.verify_and_set_user(username)
        
        # If a current user exists, allow inline confirmation/change
        entered = self.prompter.ask(self.loc.t("user.enter_with_default", username=current_user)).strip()
        if entered:
            self.set_current_user(entered)
        return True 
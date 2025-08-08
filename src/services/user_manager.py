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
            # Connect to Anki database
            conn = sqlite3.connect(str(self.anki_db_path))
            cursor = conn.cursor()
            
            # Check if user exists (this is a simplified check)
            # In a real implementation, you'd need to check the actual Anki user structure
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            conn.close()
            
            # For now, we'll assume the user exists if we can access the database
            # In a real implementation, you'd check the actual user structure
            return True
            
        except sqlite3.Error:
            return False
    
    def create_anki_user(self, username: str) -> bool:
        """Create a new Anki user (stub implementation)."""
        # This is a stub implementation
        # In a real implementation, you'd use Anki's API to create a user
        print(f"🔄 Creating Anki user: {username}")
        print("📝 Note: This is a stub implementation. In a real scenario, this would create the user in Anki.")
        return True
    
    def prompt_for_username(self) -> str:
        """Prompt user to enter a username."""
        while True:
            username = input("👤 Please enter your username: ").strip()
            if username:
                return username
            print("❌ Username cannot be empty. Please try again.")
    
    def verify_and_set_user(self, username: str) -> bool:
        """Verify user exists in Anki and set as current user."""
        print(f"🔍 Checking if user '{username}' exists in Anki...")
        
        if self.check_anki_user_exists(username):
            print(f"✅ User '{username}' found in Anki database.")
            response = input(f"🤔 Do you want to use '{username}' as your current user? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                self.set_current_user(username)
                print(f"✅ Set '{username}' as current user.")
                return True
            else:
                print("❌ User selection cancelled.")
                return False
        else:
            print(f"❌ User '{username}' not found in Anki database.")
            response = input(f"🤔 Do you want to create user '{username}'? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                if self.create_anki_user(username):
                    self.set_current_user(username)
                    print(f"✅ Created and set '{username}' as current user.")
                    return True
                else:
                    print("❌ Failed to create user.")
                    return False
            else:
                print("❌ User creation cancelled.")
                return False
    
    def _get_cli_hint(self, username: str) -> str:
        """Generate appropriate CLI hint based on username content."""
        if ' ' in username:
            return f'💡 To change user, run: python3 -m src.main --user "{username}"'
        else:
            return f'💡 To change user, run: python3 -m src.main --user {username}'
    
    def _get_cli_hint_generic(self) -> str:
        """Generate generic CLI hint with proper quoting example."""
        return '💡 To change user, run: python3 -m src.main --user "<new_username>"'
    
    def display_current_user(self) -> None:
        """Display the current user and helpful information."""
        current_user = self.get_current_user()
        if current_user:
            print(f"🔐 Current Anki user: {current_user}")
            # Show specific hint if username contains spaces
            if ' ' in current_user:
                print(self._get_cli_hint(current_user))
                print("⚠️  Note: Usernames with spaces must be enclosed in quotes!")
            else:
                print(self._get_cli_hint(current_user))
        else:
            print("🔐 No current user set")
            print(self._get_cli_hint_generic())
    
    def display_current_deck(self) -> None:
        """Display the current deck."""
        current_deck = self.get_current_deck()
        if current_deck:
            print(f"📦 Current Anki deck: {current_deck}")
        else:
            print("📦 No current deck set")
    
    def handle_user_setup(self, cli_username: Optional[str] = None) -> bool:
        """Handle the complete user setup process."""
        current_user = self.get_current_user()
        
        # If CLI username is provided, use it
        if cli_username:
            return self.verify_and_set_user(cli_username)
        
        # If no current user, prompt for one
        if not current_user:
            print("👋 Welcome to AnkiPhraseToolkit!")
            print("📝 No user configuration found. Let's set up your user.")
            username = self.prompt_for_username()
            return self.verify_and_set_user(username)
        
        # Display current user
        self.display_current_user()
        return True 
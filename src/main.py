from src.models import AnkiCard, Expression, Sentence
from src.export import AnkiExporter
from src.services import UserManager
from src.cli import CommandLineInterface
import sys


def show_about():
    print("🧠 AnkiPhraseToolkit v0.1 from Oleg Kovalyov - CLI for Phrase-Based Learning Assistant")


def prompt_deck_name():
    deck_name = input("Enter the name of your Anki deck: ").strip()
    print(f"📦 Deck name: {deck_name}")
    return deck_name


def main():
    show_about()
    
    # Initialize user management
    user_manager = UserManager()
    cli = CommandLineInterface()
    
    # Handle user setup
    cli_username = cli.get_user_argument()
    if not user_manager.handle_user_setup(cli_username):
        print("❌ User setup failed. Exiting.")
        sys.exit(1)
    
    print()  # Add spacing
    
    # Display current deck if exists
    user_manager.display_current_deck()
    
    # Prompt for deck name and save it
    deck_name = prompt_deck_name()
    user_manager.set_current_deck(deck_name)
    print(f"✅ Deck '{deck_name}' saved to configuration.")

    # Create Expression and Sentence objects
    expression = Expression("get rid of")
    expression.meaning = "Definition of the expression"
    expression.translation = "позбутися"
    expression.examples = ["Example usage of the expression."]
    
    sentence = Sentence("I need to get rid of these old clothes.", expression)
    
    # Create AnkiCard
    card = AnkiCard(expression, sentence)
    card.audio_expression_path = "audio/expression.mp3"
    card.audio_sentence_path = "audio/sentence.mp3"

    exporter = AnkiExporter()
    exporter.export([card], "anki_cards.tsv")
    print("✅ Card exported.")


if __name__ == "__main__":
    main()

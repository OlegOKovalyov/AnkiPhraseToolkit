from src.models import AnkiCard, Expression, Sentence
from src.export import AnkiExporter
from src.services import UserManager
from src.cli import CommandLineInterface
from src.version import __version__
import sys

from src.utils.localization import Localization
from src.utils.notifier import Notifier
from src.utils.prompter import Prompter

loc = Localization(lang="en")  # Пізніше тут можна буде поставити "uk"
notifier = Notifier()
prompter = Prompter(loc)


def show_about():
    notifier.system(loc.t("system.starting_app", version=__version__))


def prompt_deck_name(user_manager: UserManager):
    current_deck = user_manager.get_current_deck()
    if current_deck:
        entered = prompter.ask(loc.t("deck.enter_with_default", deckname=current_deck)).strip()
        return current_deck if entered == "" else entered
    deck_name = prompter.ask(loc.t("deck.enter")).strip()
    return deck_name


def main():
    show_about()
    
    # Initialize user management
    user_manager = UserManager()
    # Inject dependencies into user_manager
    user_manager.notifier = notifier
    user_manager.prompter = prompter
    user_manager.loc = loc

    cli = CommandLineInterface()
    
    # Handle user setup
    cli_username = cli.get_user_argument()
    if not user_manager.handle_user_setup(cli_username):
        notifier.error(loc.t("errors.user_setup_failed"))
        sys.exit(1)
    
    Notifier.blank()  # Add spacing
    
    # Prompt for deck name and save it
    deck_name = prompt_deck_name(user_manager)
    user_manager.set_current_deck(deck_name)
    notifier.success(loc.t("deck.saved", deckname=deck_name))

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
    notifier.success(loc.t("status.card_exported"))


if __name__ == "__main__":
    main()

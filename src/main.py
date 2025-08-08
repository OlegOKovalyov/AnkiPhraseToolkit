from src.models import AnkiCard
from src.export import AnkiExporter

def show_about():
#    print("=" * 40)
    print("🧠 AnkiPhraseToolkit v0.1 from Oleg Kovalyov - CLI for Phrase-Based Learning Assistant")
#    print("Author: Oleg Kovalyov")
#    print("=" * 40)

def prompt_deck_name():
    deck_name = input("Enter the name of your Anki deck: ").strip()
    print(f"📦 Deck name: {deck_name}")
    return deck_name

def main():
    show_about()
    deck_name = prompt_deck_name()

    # Temporary card to test the pipeline
    card = AnkiCard(
        expression="get rid of",
        definition="Definition of the expression",
        example_sentence="I need to get rid of these old clothes.",
        sentence_audio_path="audio/sentence.mp3",
        expression_audio_path="audio/expression.mp3",
        usage_note="Example usage of the expression.",
        translation="позбутися"
    )

    exporter = AnkiExporter()
    exporter.export_cards([card])
    print("✅ Card exported.")

if __name__ == "__main__":
    main()

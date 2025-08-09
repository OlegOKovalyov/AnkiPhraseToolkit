from colorama import Fore, Style, init
from typing import Optional

init(autoreset=True)


class Prompter:
    def __init__(self, loc=None):
        self.loc = loc

    def ask(self, prompt: str) -> str:
        """Ask user for a string without validation."""
        return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL} ")

    def confirm(self, prompt: str, default: bool = True) -> bool:
        """
        Ask for confirmation (y/n).
        If the user just presses Enter — returns the default value.
        """
        default_str = "Y/n" if default else "y/N"
        answer = input(f"{Fore.YELLOW}{prompt} [{default_str}]:{Style.RESET_ALL} ").strip().lower()
        if not answer:
            return default
        return answer in ["y", "yes"]

    def choose(self, prompt: str, options: list) -> str:
        """
        Let the user choose from options.
        Returns the chosen value or an empty string if no valid selection is made.
        """
        print(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}")
        for i, opt in enumerate(options, 1):
            print(f"  {Fore.GREEN}{i}{Style.RESET_ALL}. {opt}")
        enter_number = self.loc.t("prompter.enter_number") if self.loc else "Enter number:"
        choice = input(f"{enter_number} ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        return ""

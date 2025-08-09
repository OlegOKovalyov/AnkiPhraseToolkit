from colorama import Fore, Style, init

# Ініціалізація Colorama (щоб працювало і на Windows, і в Linux)
init(autoreset=True)

# Рівні повідомлень (префікси + кольори)
LEVELS = {
    "system":    {"prefix": "🖥️:", "color": Fore.CYAN},
    "info":      {"prefix": "ℹ️:", "color": Fore.BLUE},
    "success":   {"prefix": "✅:", "color": Fore.GREEN},
    "warning":   {"prefix": "⚠️:", "color": Fore.YELLOW},
    "error":     {"prefix": "❌:", "color": Fore.RED},
    "external_error": {"prefix": "🔌 API ERROR:", "color": Fore.MAGENTA},
}

class Notifier:
    @staticmethod
    def _print(level: str, message: str):
        """Внутрішній метод для друку повідомлень з заданим рівнем."""
        style = LEVELS.get(level, LEVELS["info"])
        print(f"{style['color']}{style['prefix']} {message}{Style.RESET_ALL}")

    @staticmethod
    def blank():
        print()

    @classmethod
    def system(cls, message: str):
        cls._print("system", message)

    @classmethod
    def info(cls, message: str):
        cls._print("info", message)

    @classmethod
    def success(cls, message: str):
        cls._print("success", message)

    @classmethod
    def warning(cls, message: str):
        cls._print("warning", message)

    @classmethod
    def error(cls, message: str):
        cls._print("error", message)

    @classmethod
    def external_error(cls, message: str):
        cls._print("external_error", message)

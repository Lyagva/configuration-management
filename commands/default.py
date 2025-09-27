import argparse


class Command:
    """
    Базовый класс для всех команд эмулятора.
    """

    @staticmethod
    def get_parser() -> argparse.ArgumentParser:
        """
        Возвращает парсер аргументов для команды.
        """
        return argparse.ArgumentParser()

    @staticmethod
    def help(self) -> str:
        """
        Возвращает строку помощи для команды.
        """
        return ""

    @staticmethod
    def execute(emulator, *args) -> None:
        """
        Точка входа для выполнения команды.
        """
        return
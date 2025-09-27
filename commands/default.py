import argparse


class Command:
    @staticmethod
    def get_parser() -> argparse.ArgumentParser:
        return argparse.ArgumentParser()

    @staticmethod
    def help(self) -> str:
        return ""

    @staticmethod
    def execute(emulator, *args) -> None:
        return
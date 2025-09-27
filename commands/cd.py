import argparse
from commands.default import Command

class Cd(Command):
    """
    Команда смены директории.
    """
    @staticmethod
    def get_parser() -> argparse.ArgumentParser:
        """
        Парсер для аргумента пути.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("path", nargs="?")
        return parser

    @staticmethod
    def execute(emulator, *args) -> None:
        """
        Смена текущей директории эмулятора.
        """
        args, unknown = Cd.get_parser().parse_known_args(args)
        target = args.path if args.path else (unknown[0] if unknown else None)
        if not target:
            return

        try:
            new_path = emulator.vfs.stepDir(emulator.path, target) if not target.startswith("/") else target
            folder = emulator.vfs._get_or_create_folder(new_path)

            from vfs import Folder
            if not isinstance(folder, Folder):
                return
            emulator.path = new_path
        except Exception as e:
            print(f"cd: {e}")
        return
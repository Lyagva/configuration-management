import argparse
from commands.default import Command

class Echo(Command):
    @staticmethod
    def get_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input")
        parser.add_argument("-o", "--output")
        return parser

    @staticmethod
    def execute(emulator, *args) -> None:
        parser = Echo.get_parser()
        parsed, unknown = parser.parse_known_args(args)
        text = " ".join(unknown)

        if parsed.input:
            folder = emulator.vfs._get_or_create_folder(emulator.path)
            file_obj = folder.content.get(parsed.input)
            if not file_obj or file_obj.__class__.__name__ != "File":
                print(f"echo: File '{parsed.input}' not found")
                return
            text = file_obj.content

        if parsed.output:
            try:
                emulator.vfs.createFile(emulator.path, parsed.output, text)
            except Exception as e:
                print(f"echo: {e}")
            return

        if text:
            print(text)
        return
from commands.default import Command

class Pwd(Command):
    @staticmethod
    def execute(emulator, *args) -> None:
        print(emulator.path)


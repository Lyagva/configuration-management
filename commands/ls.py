from commands.default import Command

class Ls(Command):
    @staticmethod
    def execute(emulator, *args) -> None:
        print("this is a placeholder for LS commands")
        return
from commands.default import Command

class Cd(Command):
    @staticmethod
    def execute(emulator, *args) -> None:
        print("this is a placeholder for CD commands")
        return
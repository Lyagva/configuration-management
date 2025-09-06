from commands.default import Command

class Exit(Command):
    @staticmethod
    def execute(emulator, *args) -> None:
        emulator.running = False
        return
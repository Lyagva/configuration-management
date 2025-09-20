from commands.default import Command

class Echo(Command):
    @staticmethod
    def execute(emulator, *args) -> None:
        print(args)
        if len(args):
            print(" ".join(args))
        return
class Command:
    @staticmethod
    def help(self) -> str:
        return ""

    @staticmethod
    def execute(emulator, *args) -> None:
        return
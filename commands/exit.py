from commands.default import Command

class Exit(Command):
    """
    Команда завершения работы эмулятора.
    """
    @staticmethod
    def execute(emulator, *args) -> None:
        """
        Завершает цикл эмулятора.
        """
        emulator.running = False
        return
from commands.default import Command

class Pwd(Command):
    """
    Команда вывода текущего пути.
    """
    @staticmethod
    def execute(emulator, *args) -> None:
        """
        Выводит текущий путь эмулятора.
        """
        print(emulator.path)

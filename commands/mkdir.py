from commands.default import Command

class Mkdir(Command):
    """
    Команда создания папки (поддерживает вложенные пути).
    """
    @staticmethod
    def execute(emulator, *args) -> None:
        """
        Создает все недостающие папки по указанному пути.
        """
        if not args or not args[0]:
            return
        path_arg = args[0]

        if path_arg.startswith("/"):
            full_path = path_arg
        else:
            full_path = emulator.path.rstrip("/") + "/" + path_arg if emulator.path != "/" else "/" + path_arg


        steps = [p for p in full_path.split("/") if p]
        current_path = ""
        for step in steps:
            current_path += "/" + step if current_path else "/" + step
            try:
                emulator.vfs._get_or_create_folder(current_path)
            except Exception as e:
                print(f"mkdir: {e}")
                return

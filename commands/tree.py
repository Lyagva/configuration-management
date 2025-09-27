from commands.default import Command

class Tree(Command):
    @staticmethod
    def execute(emulator, *args) -> None:
        from vfs import Folder
        path = args[0] if args and args[0] else emulator.path
        folder = emulator.vfs._get_or_create_folder(path)
        if not isinstance(folder, Folder):
            print(f"tree: '{path}' не является папкой")
            return
        folder.print_tree()


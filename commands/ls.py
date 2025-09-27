from commands.default import Command

class Ls(Command):
    @staticmethod
    def execute(emulator, *args) -> None:
        try:
            folder = emulator.vfs._get_or_create_folder(emulator.path)
            if not folder.content:
                return
            for name, obj in folder.content.items():
                if hasattr(obj, "content"):
                    if obj.__class__.__name__ == "Folder":
                        print(f"{name}/")
                    else:
                        print(name)
                else:
                    print(name)
        except Exception as e:
            print(f"ls: {e}")
        return
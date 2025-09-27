import argparse


class Touch:
    @staticmethod
    def get_parser() -> argparse.ArgumentParser:
        return argparse.ArgumentParser()

    @staticmethod
    def help(self) -> str:
        return ""

    @staticmethod
    def execute(emulator, *args) -> None:
        if not args or not args[0]:
            return
        full_path = args[0]
        content = " ".join(args[1:]) if len(args) > 1 else ""

        if "/" in full_path:
            *folder_parts, filename = full_path.split("/")
            folder_path = "/".join(folder_parts)

            if not full_path.startswith("/"):
                folder_path = emulator.path.rstrip("/") + "/" + folder_path if emulator.path != "/" else "/" + folder_path
            else:
                folder_path = "/" + folder_path if not folder_path.startswith("/") else folder_path
        else:
            folder_path = emulator.path
            filename = full_path
        try:
            emulator.vfs._get_or_create_folder(folder_path)
            emulator.vfs.createFile(folder_path, filename, content)
        except Exception as e:
            print(f"touch: {e}")

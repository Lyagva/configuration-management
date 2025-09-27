import os
from argparse import ArgumentParser
from datetime import datetime
from json import load, JSONEncoder
import base64

from typing import Dict, Any

class File:
    def __init__(self, name: str, content: str = "",
                 createdAt: datetime = None, modifiedAt: datetime = None):
        self.name = name
        self.createdAt = createdAt if createdAt is not None else datetime.now()
        self.modifiedAt = modifiedAt if modifiedAt is not None else datetime.now()
        self.content = content

    def getContent(self):
        return base64.b64decode(self.content)

    @staticmethod
    def load(dict_obj: Dict):
        name = dict_obj.get("name", "")
        content = dict_obj.get("content", "")
        createdAt = dict_obj.get("createdAt", None)
        modifiedAt = dict_obj.get("modifiedAt", None)

        if createdAt:
            createdAt = datetime.fromisoformat(createdAt)
        if modifiedAt:
            modifiedAt = datetime.fromisoformat(modifiedAt)

        if isinstance(content, str):
            content = content

        return File(name, content, createdAt, modifiedAt)


class Folder:
    def __init__(self, name: str,
                 createdAt: datetime = None, modifiedAt: datetime = None):
        self.name = name
        self.createdAt = createdAt if createdAt is not None else datetime.now()
        self.modifiedAt = modifiedAt if modifiedAt is not None else datetime.now()
        self.content: Dict[Any] = {}

    def addContent(self, content: Any):
        if content in self.content:
            return
        self.content[content.name] = content

    @staticmethod
    def load(dict_obj: Dict):
        name = dict_obj.get("name", "")
        createdAt = dict_obj.get("createdAt", None)
        modifiedAt = dict_obj.get("modifiedAt", None)
        if createdAt:
            createdAt = datetime.fromisoformat(createdAt)
        if modifiedAt:
            modifiedAt = datetime.fromisoformat(modifiedAt)

        folder = Folder(name, createdAt, modifiedAt)

        content_dict = dict_obj.get("content", {})
        for key, value in content_dict.items():
            if isinstance(value, dict) and "content" in value and isinstance(value["content"], str):
                folder.content[key] = File.load(value)
            elif isinstance(value, dict):
                folder.content[key] = Folder.load(value)

        return folder

    def print_tree(self, indent: int = 0):
        prefix = "    " * indent
        print(f"{prefix}[D] {self.name}")
        for item in self.content.values():
            if isinstance(item, Folder):
                item.print_tree(indent + 1)
            elif isinstance(item, File):
                print(f"{prefix}    [F] {item.name}")


class VfsEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, File):
            return {
                "name": obj.name,
                "createdAt": obj.createdAt.isoformat() if obj.createdAt else None,
                "modifiedAt": obj.modifiedAt.isoformat() if obj.modifiedAt else None,
                "content": base64.b64encode(obj.getContent()).decode("utf-8")
            }
        if isinstance(obj, Folder):
            return {
                "name": obj.name,
                "createdAt": obj.createdAt.isoformat() if obj.createdAt else None,
                "modifiedAt": obj.modifiedAt.isoformat() if obj.modifiedAt else None,
                "content": {k: self.default(v) for k, v in obj.content.items()}
            }
        return super().default(obj)


class Vfs:
    def __init__(self, filepath: str = ""):
        self.filepath = filepath

        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            with open(self.filepath, mode='r') as f:
                vfs_dict = load(f)
            self.vfs = Folder.load(vfs_dict)
        else:
            self.vfs = Folder("root")

        if not self.filepath:
            self.filepath = "vfs.json"

    def _get_or_create_folder(self, path: str) -> Folder:
        current = self.vfs
        if path == "" or path == "/":
            return current

        steps = [p for p in path.split("/") if p]
        for step in steps:
            if step not in current.content or not isinstance(current.content[step], Folder):
                current.content[step] = Folder(step)
            current = current.content[step]

        return current

    def save(self):
        from vfs import VfsEncoder
        import json

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.vfs, f, cls=VfsEncoder, ensure_ascii=False, indent=2)

    def createFile(self, path: str, filename: str = "", content: str = ""):
        if not filename or any(c in filename for c in "/\\"):
            raise ValueError("Unacceptable file name")
        folder = self._get_or_create_folder(path)
        if filename in folder.content:
            if isinstance(folder.content[filename], Folder):
                raise ValueError(f"Folder with the name '{filename}' already exists in the directory")
        file = File(filename, content, createdAt=datetime.now(), modifiedAt=datetime.now())
        folder.content[filename] = file
        self.save()
        return file

    def createFolder(self, path: str, foldername: str = ""):
        if not foldername or any(c in foldername for c in "/\\"):
            raise ValueError("Unacceptable folder name")
        parent_folder = self._get_or_create_folder(path)
        if foldername in parent_folder.content:
            if isinstance(parent_folder.content[foldername], File):
                raise ValueError(f"File with the name '{foldername}' already exists in the directory")
            self.save()
            return parent_folder.content[foldername]
        new_folder = Folder(foldername, createdAt=datetime.now(), modifiedAt=datetime.now())
        parent_folder.content[foldername] = new_folder
        self.save()
        return new_folder


    def changeDir(self, path: str, steps: str):
        if steps[0] == "/":
            steps = steps.split("/")
            steps[0] = "/"
        else:
            steps = steps.split("/")

        for step in steps:
            path = self.stepDir(path, step)
            print(path)


    def stepDir(self, path: str, step: str):
        if step == "/":
            path = "/"
            return path
        if step == ".":
            return path
        if step == "..":
            if len(path.split("/")) > 0:
                path = "/".join(path.split("/")[:-1])
            return path
        if path[-1] != "/":
            path += "/"

        return path + step


if __name__ == "__main__":
    vfs = Vfs()
    print("\n--- Тест: создание папок ---")
    folder_a = vfs.createFolder("", "A")
    folder_b = vfs.createFolder("A", "B")
    folder_c = vfs.createFolder("A/B", "C")
    print("Папки созданы:", list(vfs.vfs.content.keys()))
    print("Вложенные папки A:", list(folder_a.content.keys()))
    print("Вложенные папки B:", list(folder_b.content.keys()))

    print("\n--- Тест: создание файлов ---")
    file1 = vfs.createFile("A/B/C", "file1.txt", "Hello from file1!")
    file2 = vfs.createFile("A/B", "file2.txt", "Hello from file2!")
    print("Файлы в папке C:", list(folder_c.content.keys()))
    print("Файлы в папке B:", list(folder_b.content.keys()))

    print("\n--- Тест: проверка содержимого файла ---")
    print("file1.txt content:", file1.content)
    print("file2.txt content:", file2.content)

    print("\n--- Тест: вложенность ---")
    assert "B" in folder_a.content
    assert "C" in folder_b.content
    assert "file1.txt" in folder_c.content
    assert "file2.txt" in folder_b.content
    print("Вложенность работает корректно!")

    print("\n--- Тест: вывод дерева ---")
    vfs.vfs.print_tree()
    print("--- Тест завершён ---")

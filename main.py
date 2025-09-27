import os, sys, platform, argparse, sys

from commands import ls, cd, default, exit, echo, touch, pwd, mkdir, tree
from typing import List, Dict, TypeVar, Any
from vfs import Vfs


parser = argparse.ArgumentParser(
    prog="Custom terminal emulator",
)
parser.add_argument("-vfs", help="Path to virtual file system")
parser.add_argument("-s", help="Path to startup script")

class Args:
    """
    Вспомогательный класс для хранения аргументов командной строки.
    """
    pass


class Emulator:
    """
    Основной класс эмулятора терминала.
    Реализует обработку команд, работу с виртуальной ФС, запуск скриптов, хранит состояние эмулятора.
    """
    def __init__(self, args) -> None:
        """
        Инициализация эмулятора, загрузка ФС, настройка команд.
        """
        self.args = args
        self.os = sys.platform
        self.running = True
        self.path = "/"
        self.vfs = Vfs(args.vfs) if getattr(args, "vfs", None) else Vfs()

        self.aliases: Dict[str, Any(default.Command)] = {
            "ls": ls.Ls,
            "cd": cd.Cd,
            "echo": echo.Echo,
            "exit": exit.Exit,
            "touch": touch.Touch,
            "pwd": pwd.Pwd,
            "mkdir": mkdir.Mkdir,
            "tree": tree.Tree
        }


        print(f"Args:\n\t" + " ".join(sys.argv[1:]) + "\n")
        if args.s and os.path.exists(args.s):
            with open(args.s, "r") as f:
                for line in f.readlines():
                    line = line.strip().split(" ")
                    print(self.getPrompt() + " ".join(line))
                    self.executeCommand(line[0], line[1:])

    def getEnvVar(self, name: str) -> str | None:
        """
        Возвращает значение переменной окружения по имени.
        """
        name = name.replace("$", "")
        try:
            return str(os.environ[name])
        except KeyError:
            return ""

    def getHostName(self):
        return platform.uname().node

    def getPrompt(self) -> str:
        host = self.getHostName()

        user = os.getlogin()
        if not user:
            user = ""
        return f"{host}:{user}:~# "

    def findCommand(self, name: str) -> default.Command:
        if name in self.aliases:
            return self.aliases[name]
        return None

    def executeCommand(self, command, args) -> None:
        if command[0] == "$":
            command = self.getEnvVar(command)

        for i in range(len(args)):
            if args[i][0] == "$":
                args[i] = self.getEnvVar(args[i])

        command = self.findCommand(command)
        if command:
            try:
                command.execute(self, *args)
            except Exception as e:
                print(e)
            return

        print(f"Can't execute '{command}'.")

    def loop(self):
        while self.running:
            print(self.getPrompt(), end="")
            prompt = input().strip()

            if len(prompt) == 0:
                continue

            prompt = prompt.split(" ")

            self.executeCommand(prompt[0], prompt[1:])


if __name__ == "__main__":
    args = Args()
    parser.parse_args(namespace=args)
    e = Emulator(args)
    e.loop()
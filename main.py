import os, sys

from commands import ls, cd, default, exit

from typing import List, Dict, TypeVar

class Emulator:
    def __init__(self) -> None:
        self.os = sys.platform
        self.running = True

        self.aliases: Dict[str, default.Command] = {
            "ls": ls.Ls,
            "cd": cd.Cd,
            "exit": exit.Exit,
        }

    def getEnvVar(self, name: str) -> str | None:
        try:
            return os.environ[name]
        except KeyError:
            return None

    def getHostName(self):
        return os.uname().nodename

    def getPrompt(self) -> str:
        host = self.getHostName()

        user = os.getenv("USER")
        if not user:
            user = ""
        return f"{host}:{user}:~# "

    def findCommand(self, name: str) -> default.Command:
        if name in self.aliases:
            return self.aliases[name]
        return None

    def loop(self):
        while self.running:
            print(self.getPrompt(), end="")
            prompt = input().strip()

            if len(prompt) == 0:
                continue
            elif prompt[0] == "$":
                print(self.getEnvVar(prompt[1:]))
                continue

            prompt = prompt.split(" ")

            command = self.findCommand(prompt[0])
            if command:
                command.execute(self, *(prompt[1:]))
                continue
            else:
                print(f"Can't find '{prompt}'.")


if __name__ == "__main__":
    e = Emulator()
    e.loop()
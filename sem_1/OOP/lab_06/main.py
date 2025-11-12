from abc import ABC, abstractmethod
import string
from typing import Optional, Callable
from pathlib import Path
import json

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...
    
    @abstractmethod
    def cancel(self) -> None:
        ...

class Keyboard:
    def __init__(self, file_to_safe: str) -> None:
        self.state_server = KeybordStateSaver(self, file_to_safe)
        self.undo_stack = []
        self.redo_stack = []
        self.printed_sq = ""
        self.commands = {}

    def init_commands(self, commands: dict[str, Command]) -> None:
        self.commands = commands

    def do(self, command_key: str) -> None:
        if command_key not in self.commands:
            print(f"Command '{command_key}' not found")
            return
        cmd = self.commands[command_key]
        cmd.execute()
        self.undo_stack.append(command_key)
        self.redo_stack.clear()

    def undo(self) -> None:
        if not self.undo_stack:
            print("Nothing to undo")
            return
        command_key = self.undo_stack.pop()
        cmd = self.commands[command_key]
        cmd.cancel()
        self.redo_stack.append(command_key)

    def redo(self) -> None:
        if not self.redo_stack:
            print("Nothing to redo")
            return
        command_key = self.redo_stack.pop()
        cmd = self.commands[command_key]
        cmd.execute()
        self.undo_stack.append(command_key)

    def serialize(self) -> None:
        self.state_server.save()

    def deserialize(self) -> None:
        self.state_server.load()


class KeyCommand(Command):
    def __init__(self, key: str, action: Callable[[str], None], undo_action: Callable[[], None]) -> None:
        self.key = key
        self.action = action
        self.undo_action = undo_action

    def execute(self) -> None:
        self.action(self.key)

    def cancel(self) -> None:
        self.undo_action()


class VolumeUpCommand(Command):
    def __init__(self, action: Callable[[], None], undo_action: Callable[[], None]) -> None:
        self.action = action
        self.undo_action = undo_action

    def execute(self) -> None:
        self.action()

    def cancel(self) -> None:
        self.undo_action()


class VolumeDownCommand(Command):
    def __init__(self, action: Callable[[], None], undo_action: Callable[[], None]) -> None:
        self.action = action
        self.undo_action = undo_action

    def execute(self) -> None:
        self.action()

    def cancel(self) -> None:
        self.undo_action()


class MediaPlayerCommand(Command):
    def __init__(self, action: Callable[[], None], undo_action: Callable[[], None]) -> None:
        self.action = action
        self.undo_action = undo_action

    def execute(self) -> None:
        self.action()

    def cancel(self) -> None:
        self.undo_action()

class KeybordStateSaver:
    def __init__(self, keyboard: Keyboard, file_path: str) -> None:
        self.keyboard = keyboard
        self.file_path = Path(file_path)

    def save(self) -> None:
        commands_data = {}
        for key, cmd in self.keyboard.commands.items():
            data = {k: v for k, v in cmd.__dict__.items() if k not in ("keyboard", "action", "undo_action")}
            commands_data[key] = {
                "type": cmd.__class__.__name__,
                "args": data
            }

        full_data = {
            "printed_sq": self.keyboard.printed_sq,
            "undo_stack": self.keyboard.undo_stack,
            "redo_stack": self.keyboard.redo_stack,
            "commands": commands_data
        }

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(full_data, f, indent=4, ensure_ascii=False)

    def load(self) -> None:
        if not self.file_path.exists():
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.keyboard.printed_sq = data.get("printed_sq", "")
        self.keyboard.undo_stack = data.get("undo_stack", [])
        self.keyboard.redo_stack = data.get("redo_stack", [])

        commands_data = data.get("commands", {})
        restored = {}

        for key, info in commands_data.items():
            cmd_type = info["type"]
            args = info["args"]

            if cmd_type == "KeyCommand":
                restored[key] = KeyCommand(
                    args["key"],
                    action=lambda k=args["key"], kb=self.keyboard: setattr(kb, "printed_sq", kb.printed_sq + k) or print(kb.printed_sq),
                    undo_action=lambda kb=self.keyboard: setattr(kb, "printed_sq", kb.printed_sq[:-1]) or print(kb.printed_sq)
                )
            elif cmd_type == "VolumeUpCommand":
                restored[key] = VolumeUpCommand(
                    action=lambda: print("volume increased +20%"),
                    undo_action=lambda: print("volume decreased -20%")
                )
            elif cmd_type == "VolumeDownCommand":
                restored[key] = VolumeDownCommand(
                    action=lambda: print("volume decreased +20%"),
                    undo_action=lambda: print("volume increased -20%")
                )
            elif cmd_type == "MediaPlayerCommand":
                restored[key] = MediaPlayerCommand(
                    action=lambda: print("media player launched"),
                    undo_action=lambda: print("media player closed")
                )

        self.keyboard.init_commands(restored)

from pathlib import Path

TEST_FILE = "test_state.json"

k = Keyboard(TEST_FILE)

commands = {
    letter: KeyCommand(
        letter,
        action=lambda key=letter, k=k: setattr(k, 'printed_sq', k.printed_sq + key) or print(k.printed_sq),
        undo_action=lambda k=k: setattr(k, 'printed_sq', k.printed_sq[:-1]) or print(k.printed_sq)
    )
    for letter in "abcd"
}

commands["ctrl++"] = VolumeUpCommand(
    action=lambda: print("volume increased +20%"),
    undo_action=lambda: print("volume decreased -20%")
)

commands["ctrl+-"] = VolumeDownCommand(
    action=lambda: print("volume decreased +20%"),
    undo_action=lambda: print("volume increased -20%")
)

commands["ctrl+p"] = MediaPlayerCommand(
    action=lambda: print("media player launched"),
    undo_action=lambda: print("media player closed")
)

k.init_commands(commands)

# --- Тест 1: Печать символов и undo/redo ---
print("== Test 1: Print and Undo/Redo ==")
k.do('a')  # a
k.do('b')  # ab
k.do('c')  # abc
k.undo()   # ab
k.undo()   # a
k.redo()   # ab

# --- Тест 2: Команды громкости ---
print("== Test 2: Volume Commands ==")
k.do('ctrl++')  # volume increased +20%
k.undo()        # volume decreased -20%
k.do('ctrl+-')  # volume decreased +20%
k.undo()        # volume increased -20%

# --- Тест 3: Команда медиаплеера ---
print("== Test 3: Media Player Command ==")
k.do('ctrl+p')  # media player launched
k.undo()        # media player closed

# --- Тест 4: Сохранение состояния ---
print("== Test 4: Save State ==")
k.serialize()  # сохраняем состояние

# --- Тест 5: Восстановление состояния ---
print("== Test 5: Load State ==")
new_k = Keyboard(TEST_FILE)
new_k.deserialize()

# Проверка восстановления строки
print(f"Restored printed_sq: {new_k.printed_sq}")  # должно быть 'ab'
print(f"Restored undo_stack: {new_k.undo_stack}")  # должно содержать историю команд

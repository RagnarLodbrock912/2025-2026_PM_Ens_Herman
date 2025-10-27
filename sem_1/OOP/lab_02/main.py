from enum import Enum
from typing import Self
import types

from font_7 import font7
from font_5 import font5


class Color(Enum):
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

class Printer:
    def __init__(self, color: Color, position: tuple[int, int], symbol: str, font: dict[str, list]) -> None:
        self.color = color
        self.position = position
        self.symbol = symbol
        self.font = font

    @classmethod
    def print_text(cls, text: str, color: Color, position: tuple[int, int], symbol: str, font: dict[str, list]) -> None:
        P = cls(color, position, symbol, font)
        P.print(text)

    def print(self, text) -> None:
        x, y = self.position

        print("\n" * x, end="")

        for string in text.split("\n"):
            formatted_text = list()

            for s in string:
                formatted_text.append(self.font[s.upper()])
                formatted_text.append(self.font[" "])

            if len(formatted_text) == 0:
                print()
                continue

            new_rows = [""] * len(formatted_text[0])

            for el in formatted_text:
                for i, row in enumerate(el):
                    new_rows[i] += row
            
            for i, row in enumerate(new_rows):
                print(" " * y + self.color.value + row.replace("*", self.symbol) + Color.RESET.value)
            
            print()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, 
        exc_type: type | None, 
        exc_value: BaseException | None, 
        traceback: types.TracebackType | None
    ) -> None:
        print(Color.RESET.value, end="")


Printer.print_text("Hello", Color.MAGENTA, (2,5), "#", font5)

with Printer(Color.GREEN, (1,1), "8", font7) as p:
    p.print("Hello, \n World")
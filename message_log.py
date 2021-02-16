from typing import List, Reversible, Tuple
import textwrap
import tcod
import color

class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        """the full message, including the count if necessary"""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        else:
            return self.plain_text

class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] =[]

    def add_message(
        self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True,
    ) -> None:
        """add a message to this log
        `text` - the message text
        `fg` - foreground color, text color
        `stack` - if true, message can stack with previous message of same text
        """

        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
        self, console: tcod.Console, x: int, y: int, width: int, height: int,
   ) -> None:
        """render this log over the given area"""
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def render_messages(
            console: tcod.Console,
            x: int,
            y: int,
            width: int,
            height: int,
            messages: Reversible[Message],
    ) -> None:
        y_offset = height - 1
        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return
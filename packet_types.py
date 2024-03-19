"""This module contains the definitions of packet types."""

from typing import NamedTuple

class Color(NamedTuple):
    """A named tuple representing a color."""

    a: int
    r: int
    g: int
    b: int

class ChatItem(NamedTuple):
    """A named tuple representing a chat item."""

    color: Color
    owner_id: int
    text: str
    icon: str

class Position(NamedTuple):
    """A named tuple representing a position."""

    x: float
    y: float

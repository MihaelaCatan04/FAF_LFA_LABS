from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    RECIPE = auto()
    TITLE = auto()
    INGREDIENT = auto()
    STEP = auto()
    YIELD = auto()
    TIME = auto()
    TEMP = auto()

    # Literals
    STRING = auto()
    NUMBER = auto()

    # Units
    UNIT = auto()
    TIME_UNIT = auto()
    TEMP_UNIT = auto()

    # Identifiers
    ID = auto()

    # Symbols
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    LBRACE = auto()
    RBRACE = auto()

    # Special
    EOF = auto()
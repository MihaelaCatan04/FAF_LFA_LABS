import re
from Token import Token
from TokenType import TokenType


class Lexer:
    def __init__(self):
        self.tokens = []
        self.token_patterns = [
            (TokenType.RECIPE, r'RECIPE'),
            (TokenType.TITLE, r'TITLE'),
            (TokenType.INGREDIENT, r'INGREDIENT'),
            (TokenType.STEP, r'STEP'),
            (TokenType.YIELD, r'YIELD'),
            (TokenType.TIME, r'TIME'),
            (TokenType.TEMP, r'TEMP'),
            (TokenType.STRING, r'"[^"]*"'),
            (TokenType.NUMBER, r'[0-9]+(\.[0-9]+)?'),
            (TokenType.UNIT, r'(g|ml|tsp|tbsp|cup)'),
            (TokenType.TIME_UNIT, r'(min|hr)'),
            (TokenType.TEMP_UNIT, r'(C|F)'),
            (TokenType.ID, r'[a-zA-Z][a-zA-Z0-9_]*'),
            (TokenType.COLON, r':'),
            (TokenType.SEMICOLON, r';'),
            (TokenType.COMMA, r','),
            (TokenType.LBRACE, r'{'),
            (TokenType.RBRACE, r'}'),
            (None, r'[ \t\n]+')  # Whitespace is ignored
        ]

    def tokenize(self, text):
        self.tokens = []
        position = 0

        while position < len(text):
            match_found = False

            for token_type, pattern in self.token_patterns:
                regex = re.compile(f'^{pattern}', re.IGNORECASE)
                match = regex.match(text[position:])

                if match:
                    value = match.group(0)

                    if token_type is not None:  # Skip whitespace
                        self.tokens.append(Token(token_type, value))

                    position += len(value)
                    match_found = True
                    break

            if not match_found:
                raise ValueError(f"Unrecognized token at position {position}: '{text[position:position + 10]}'")

        self.tokens.append(Token(TokenType.EOF, ''))
        return self.tokens
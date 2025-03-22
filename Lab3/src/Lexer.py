import re
from Token import Token


class Lexer:
    def __init__(self):
        self.tokens = []
        self.token_patterns = {
            'KEYWORD': r'(RECIPE|TITLE|INGREDIENT|STEP|YIELD|TIME|TEMP)',
            'STRING': r'"[^"]*"',
            'NUMBER': r'[0-9]+(\.[0-9]+)?',
            'UNIT': r'(g|ml|tsp|tbsp|cup)',
            'TIME_UNIT': r'(min|hr)',
            'TEMP_UNIT': r'(C|F)',
            'ID': r'[a-zA-Z][a-zA-Z0-9_]*',
            'COLON': r':',
            'SEMICOLON': r';',
            'COMMA': r',',
            'LBRACE': r'{',
            'RBRACE': r'}',
            'WHITESPACE': r'[ \t\n]+'
        }

    def tokenize(self, text):
        self.tokens = []
        position = 0
        while position < len(text):
            match_found = False

            for token_type, pattern in self.token_patterns.items():
                regex = re.compile(f'^{pattern}', re.IGNORECASE)
                match = regex.match(text[position:])

                if match:
                    value = match.group(0)

                    if token_type != 'WHITESPACE':
                        self.tokens.append(Token(token_type, value))

                    position += len(value)
                    match_found = True
                    break

            if not match_found:
                raise ValueError(f"Unrecognized token at position {position}: '{text[position:position + 10]}'")

        self.tokens.append(Token('EOF', ''))
        return self.tokens
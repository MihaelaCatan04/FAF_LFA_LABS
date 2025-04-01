import re
from RegexLogger import RegexLogger


class RegexParser:
    def __init__(self):
        self.tokens = []
        self.logger = RegexLogger()

    def parse(self, pattern):
        self.logger = RegexLogger() 
        self.logger.process(f"Parsing pattern: {pattern}")
        self.tokens = []
        i = 0

        while i < len(pattern):
            char = pattern[i]

            # Handle groupings
            if char == "(":
                group_end = pattern.find(")", i)
                if group_end != -1:
                    # Check if followed by repetition
                    if group_end + 1 < len(pattern) and pattern[group_end + 1] == "^":
                        match = re.match(r"\((.*?)\)\^\{(\d+)\}", pattern[i:])
                        if match:
                            group_content = match.group(1).split('|')
                            repetition = int(match.group(2))
                            self.tokens.append(('group', (group_content, repetition)))
                            i += len(match.group(0))
                            self.logger.process(f"Found group with repetition: {match.group(0)}")
                            continue
                    # Simple group with modifiers
                    elif group_end + 1 < len(pattern) and pattern[group_end + 1] in "?*+":
                        group_content = pattern[i + 1:group_end].split('|')
                        modifier = pattern[group_end + 1]
                        self.tokens.append(('group_mod', (group_content, modifier)))
                        i = group_end + 2
                        self.logger.process(f"Found group with modifier: ({pattern[i + 1:group_end]}){modifier}")
                        continue
                    else:
                        # Simple group without modifiers
                        self.logger.process(f"Found simple group: ({pattern[i + 1:group_end]})")
                        group_content = pattern[i + 1:group_end].split('|')
                        self.tokens.append(('group', (group_content, 1)))
                        i = group_end + 1
                        continue

            # Character with repetition
            if i + 1 < len(pattern) and pattern[i + 1] == "^":
                match = re.match(r"(\w)\^\{(\d+)\}", pattern[i:])
                if match:
                    char = match.group(1)
                    repetition = int(match.group(2))
                    self.tokens.append(('char_rep', (char, repetition)))
                    i += len(match.group(0))
                    self.logger.process(f"Found character with repetition: {match.group(0)}")
                    continue

            # Character with modifier (?, *, +)
            if i + 1 < len(pattern) and pattern[i + 1] in "?*+":
                modifier = pattern[i + 1]
                self.tokens.append(('char_mod', (char, modifier)))
                i += 2
                self.logger.process(f"Found character with modifier: {char}{modifier}")
                continue

            # Simple character
            self.tokens.append(('char', char))
            self.logger.process(f"Found simple character: {char}")
            i += 1

        return self.tokens

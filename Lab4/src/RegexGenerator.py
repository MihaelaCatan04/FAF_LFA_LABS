import itertools
from RegexLogger import RegexLogger


class RegexGenerator:
    def __init__(self):
        self.logger = RegexLogger()

    def generate(self, tokens):
        self.logger = RegexLogger()
        result_parts = []

        for token_type, token_value in tokens:
            self.logger.process(f"Processing token: {token_type} - {token_value}")

            if token_type == 'char':
                # Simple character
                result_parts.append([token_value])

            elif token_type == 'char_rep':
                # Character with repetition
                char, repetition = token_value
                result_parts.append([char * repetition])
                self.logger.process(f"Generated repeated character: {char * repetition}")

            elif token_type == 'char_mod':
                # Character with modifier
                char, modifier = token_value
                if modifier == '?':
                    # Optional (0 or 1)
                    result_parts.append(['', char])
                    self.logger.process(f"Generated optional character: '' or '{char}'")
                elif modifier == '*':
                    # Zero or more (limit to 5)
                    result_parts.append([char * i for i in range(6)])
                    self.logger.process(f"Generated 0-5 repetitions of '{char}'")
                elif modifier == '+':
                    # One or more (limit to 5)
                    result_parts.append([char * i for i in range(1, 6)])
                    self.logger.process(f"Generated 1-5 repetitions of '{char}'")

            elif token_type == 'group':
                # Group with repetition
                options, repetition = token_value
                if repetition == 1:
                    # Group without repetition
                    result_parts.append(options)
                    self.logger.process(f"Generated group options: {options}")
                else:
                    # Group with repetition
                    combinations = []
                    for combo in itertools.product(options, repeat=repetition):
                        combinations.append(''.join(combo))
                    result_parts.append(combinations)
                    self.logger.process(
                        f"Generated group repetitions: {combinations[:5]}{'...' if len(combinations) > 5 else ''}")

            elif token_type == 'group_mod':
                # Group with modifier
                options, modifier = token_value
                if modifier == '?':
                    # Optional group (0 or 1)
                    result_parts.append([''] + options)
                    self.logger.process(f"Generated optional group: '' or {options}")
                elif modifier == '*':
                    # Zero or more (limit to 5)
                    combinations = ['']
                    for i in range(1, 6):
                        for combo in itertools.product(options, repeat=i):
                            combinations.append(''.join(combo))
                    result_parts.append(combinations)
                    self.logger.process(f"Generated 0-5 group repetitions")
                elif modifier == '+':
                    # One or more (limit to 5)
                    combinations = []
                    for i in range(1, 6):
                        for combo in itertools.product(options, repeat=i):
                            combinations.append(''.join(combo))
                    result_parts.append(combinations)
                    self.logger.process(f"Generated 1-5 group repetitions")

        # Generate all combinations
        self.logger.process("Generating final combinations...")
        all_combinations = []

        # Combine all parts
        for combo in itertools.product(*result_parts):
            all_combinations.append(''.join(combo))

        self.logger.process(f"Generated {len(all_combinations)} total combinations")
        return all_combinations
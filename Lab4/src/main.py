from RegexParser import RegexParser
from RegexGenerator import RegexGenerator

patterns = [
    "M?N^{2}(O|P)^{3}O*R+",
    "(X|Y|Z)^{3}8+(9|0)^{2}",
    "(H|i)(J|L)L*N?"
]

parser = RegexParser()
generator = RegexGenerator()

file_path = "../additional_files/regex_combinations.txt"
with open(file_path, "a") as f:
    for pattern in patterns:
        tokens = parser.parse(pattern)
        results = generator.generate(tokens)

        # Write the pattern and the combinations
        f.write(f"Pattern: {pattern}\n")
        for combo in results:
            f.write(combo + "\n")

        # Show log steps
        print("\nLog steps:")
        parser.logger.show_steps()
        generator.logger.show_steps()

        print("\nSample combinations:")
        for sample in results[:5]:
            print(sample)

        print(f"All combinations saved to {file_path}")

class RegexLogger:
    def __init__(self):
        self.steps = []

    def process(self, step):
        self.steps.append(step)

    def show_steps(self):
        for i, step in enumerate(self.steps, 1):
            print(f"Step {i}: {step}")
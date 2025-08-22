from metaflow import step, FlowSpec, card, Parameter


class RecursiveConditionalFlow1(FlowSpec):
    should_loop = Parameter("should_loop", default=True)
    max_recursion = Parameter("max_recursion", default=3)

    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"
        self.continue_loop = "loop" if self.should_loop else "break"
        self.iterations = 0

        self.next(self.recursive_step)

    @step
    def recursive_step(self):
        print("Starting 👋")

        self.test_value = "start"

        if self.iterations < self.max_recursion:
            self.iterations += 1
            self.continue_loop = "loop"
        else:
            self.continue_loop = "break"

        self.next(
            {"break": self.branch_a, "loop": self.recursive_step},
            condition="continue_loop",
        )

    @step
    def branch_a(self):
        print("Now in Branch A")
        self.test_value = "Went through branch A"

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")

        print(self.test_value)


if __name__ == "__main__":
    RecursiveConditionalFlow1()

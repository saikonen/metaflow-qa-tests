from metaflow import step, FlowSpec, card, Parameter


# a conditional branch in a conditional branch
class NestedConditionalFlow1(FlowSpec):
    first_branch = Parameter("first_condition", default="false")
    second_branch = Parameter("second_condition", default="false")

    @card
    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"

        self.next(
            {"true": self.branch_a, "false": self.branch_b}, condition="first_branch"
        )

    @step
    def branch_a(self):
        print("Now in Branch A")
        self.test_value = "Went through branch A"

        self.next(self.end)

    @step
    def branch_b(self):
        print("Now in Branch B")
        self.test_value = "Went through branch B"

        self.next(
            {"true": self.branch_c, "false": self.branch_d}, condition="second_branch"
        )

    @step
    def branch_c(self):
        print("Now in Branch C")
        self.test_value = "Went through branch C"

        self.next(self.end)

    @step
    def branch_d(self):
        print("Now in Branch D")
        self.test_value = "Went through branch D"

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")

        print(self.test_value)


if __name__ == "__main__":
    NestedConditionalFlow1()

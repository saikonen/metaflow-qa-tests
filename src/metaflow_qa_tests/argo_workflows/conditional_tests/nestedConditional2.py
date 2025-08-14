from metaflow import step, FlowSpec, card, Parameter


# A conditional branch in a static split
class NestedConditionalFlow2(FlowSpec):
    first_branch = Parameter("first_condition", default="false")

    @card
    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"

        self.next(self.branch_a, self.branch_b)

    @step
    def branch_a(self):
        print("Now in Branch A")
        self.test_value = "Went through branch A"

        self.next(self.join_ab)

    @step
    def branch_b(self):
        print("Now in Branch B")
        self.test_value = "Went through branch B"

        self.next(
            {"true": self.branch_c, "false": self.branch_d}, condition="first_branch"
        )

    @step
    def branch_c(self):
        print("Now in Branch C")
        self.test_value = "Went through branch C"

        self.next(self.join_ab)

    @step
    def branch_d(self):
        print("Now in Branch D")
        self.test_value = "Went through branch D"

        self.next(self.join_ab)

    @step
    def join_ab(self, inputs):
        for input in inputs:
            print(input["test_value"])
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    NestedConditionalFlow2()

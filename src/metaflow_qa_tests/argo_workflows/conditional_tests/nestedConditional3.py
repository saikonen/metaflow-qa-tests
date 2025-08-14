from metaflow import step, FlowSpec, card, Parameter


# A conditional branch in a foreach split
class NestedConditionalFlow3(FlowSpec):
    first_branch = Parameter("first_condition", default="false")

    @card
    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"
        self.items = [1, 2]

        self.next(self.split_work, foreach="items")

    @step
    def split_work(self):
        print("Now in Branch B")
        self.test_value = "Went through split_work"

        self.next(
            {"true": self.branch_c, "false": self.branch_d}, condition="first_branch"
        )

    @step
    def branch_c(self):
        print("Now in Branch C")
        self.test_value = "Went through branch C"

        self.next(self.join_c_or_d)

    @step
    def branch_d(self):
        print("Now in Branch D")
        self.test_value = "Went through branch D"

        self.next(self.join_c_or_d)

    @step
    def join_c_or_d(self, inputs):
        for input in inputs:
            print(input.test_value)
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    NestedConditionalFlow3()

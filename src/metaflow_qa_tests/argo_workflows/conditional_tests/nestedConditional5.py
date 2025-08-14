from metaflow import step, FlowSpec, card, Parameter


# A foreach split in a conditional branch
class NestedConditionalFlow5(FlowSpec):
    first_branch = Parameter("first_condition", default="false")

    @card
    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"
        self.items = [1, 2]

        self.next(
            {"true": self.branch_a, "false": self.branch_b}, condition="first_branch"
        )

    @step
    def branch_a(self):
        print("Now in Branch a")
        self.test_value = "Went through branch A"

        self.next(self.end)

    @step
    def branch_b(self):
        print("Now in Branch B")
        self.test_value = "Went through branch B"

        self.next(self.work, foreach="items")

    @step
    def work(self):
        print("Now in Branch split_work")
        self.test_value = "Went through 'work'"

        self.next(self.join_work)

    @step
    def join_work(self, inputs):
        for input in inputs:
            print(input["test_value"])
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    NestedConditionalFlow5()

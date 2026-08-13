from metaflow import step, FlowSpec, card, Parameter


class ConditionalSkipFlow2(FlowSpec):
    conditional_value = Parameter("condition", default="false")

    @card
    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"

        self.next(
            {"true": self.branch_a, "false": self.common_c},
            condition="conditional_value",
        )

    @step
    def branch_a(self):
        print("Now in Branch A")
        self.test_value = "Went through branch A"

        self.next(self.common_c)

    @step
    def common_c(self):
        print("Now in Branch A")
        self.test_value = "Went through branch A"

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")

        print(self.test_value)


if __name__ == "__main__":
    ConditionalSkipFlow2()

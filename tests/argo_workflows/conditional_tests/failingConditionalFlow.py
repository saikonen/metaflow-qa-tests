from metaflow import step, FlowSpec, Parameter, catch


# applying the catch decorator to a conditional switch step should not be allowed.
class ConditionalSwitchWithCatch(FlowSpec):
    conditional_value = Parameter("condition", default="false")

    @catch(var="test_fail")
    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"

        self.next(
            {"true": self.branch_a, "false": self.branch_b},
            condition="conditional_value",
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

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")

        print(self.test_value)


if __name__ == "__main__":
    ConditionalSwitchWithCatch()

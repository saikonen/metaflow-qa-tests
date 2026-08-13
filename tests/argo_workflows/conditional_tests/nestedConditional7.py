from metaflow import step, FlowSpec, Parameter, parallel, current


# a parallel step within a conditional step
class NestedConditionalFlow7(FlowSpec):
    condition = Parameter("condition", default="false")

    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"

        self.next(
            {"true": self.branch_a, "false": self.branch_b}, condition="condition"
        )

    @step
    def branch_a(self):
        print("Now in Branch A")
        self.test_value = "Went through branch A"

        self.next(self.a_or_b)

    @step
    def branch_b(self):
        print("Now in Branch B")
        self.test_value = "Went through branch B"

        self.next(self.parallel_work, num_parallel=2)

    @parallel
    @step
    def parallel_work(self):
        print("Now in parallel_work")
        self.parallel_test = f"Went through parallel_work {current.parallel.node_index}"

        self.next(self.parallel_join)

    @step
    def parallel_join(self, inputs):
        self.merge_artifacts(inputs, exclude=["parallel_test"])
        for input in inputs:
            self.test_value += f"{input.parallel_test}\n"
            print(input.parallel_test)

        self.next(self.a_or_b)

    @step
    def a_or_b(self):
        print(self.test_value)

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    NestedConditionalFlow7()

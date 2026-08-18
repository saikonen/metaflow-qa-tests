from metaflow import step, FlowSpec, Parameter, parallel, current


# a conditional step within a parallel
# NOTE: This is not supposed to be supported.
class NestedConditionalFlow8(FlowSpec):
    condition = Parameter("condition", default="false")

    @step
    def start(self):
        print("Starting 👋")

        self.test_value = "start"

        self.next(self.parallel_work, num_parallel=2)

    @parallel
    @step
    def parallel_work(self):
        print("Now in parallel_work")
        self.parallel_test = f"Went through parallel_work {current.parallel.node_index}"

        self.next(
            {"true": self.parallel_join_a, "false": self.parallel_join_b},
            condition="condition",
        )

    @step
    def parallel_join_a(self, inputs):
        self.merge_artifacts(inputs, exclude=["parallel_test"])
        for input in inputs:
            self.test_value += f"{input.parallel_test}\n"
            print(input.parallel_test)

        self.next(self.end)

    @step
    def parallel_join_b(self, inputs):
        self.merge_artifacts(inputs, exclude=["parallel_test"])
        for input in inputs:
            self.test_value += f"{input.parallel_test}\n"
            print(input.parallel_test)

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")
        print(self.test_value)


if __name__ == "__main__":
    NestedConditionalFlow8()

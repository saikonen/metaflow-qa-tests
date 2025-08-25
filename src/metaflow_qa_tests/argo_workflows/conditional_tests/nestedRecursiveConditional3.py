from metaflow import step, FlowSpec, parallel, current, Parameter


# a @parallel step that is a recursive conditional
# NOTE: This is not supported.
class NestedRecursiveConditionalFlow3(FlowSpec):
    should_loop = Parameter("should_loop", default=True)
    max_recursion = Parameter("max_recursion", default=3)

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
        self.case = "A"
        self.next({"A": self.parallel_join, "B": self.alternate_join}, condition="case")

    @step
    def parallel_join(self, inputs):
        self.merge_artifacts(inputs, exclude=["parallel_test"])
        for input in inputs:
            self.test_value += f"{input.parallel_test}\n"
            print(input.parallel_test)

        self.next(self.a_or_b)

    @step
    def alternate_join(self, inputs):
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
    NestedRecursiveConditionalFlow3()

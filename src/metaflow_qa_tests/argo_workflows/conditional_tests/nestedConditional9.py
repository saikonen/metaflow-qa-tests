from metaflow import FlowSpec, step


# Another example of a conditional within a conditional.
# Coverage for graph parsing failures due to reaching the end step too early.
class NestedConditionalFlow9(FlowSpec):
    @step
    def start(self):
        self.next(self.prep)

    @step
    def prep(self):
        self.prep_cond = "skip_123"
        self.next(
            {"part_1": self.part_1, "skip_123": self.skip_part_1_2_3},
            condition="prep_cond",
        )

    @step
    def part_1(self):
        self.next(self.part_2)

    @step
    def part_2(self):
        self.part_2_cond = "skip_3"
        self.next(
            {"part_3": self.part_3, "skip_3": self.skip_part_3}, condition="part_2_cond"
        )

    @step
    def part_3(self):
        self.next(self.before_end)

    @step
    def skip_part_3(self):
        self.next(self.before_end)

    @step
    def skip_part_1_2_3(self):
        self.next(self.before_end)

    @step
    def before_end(self):
        self.next(self.end)

    @step
    def end(self):
        print("end")


if __name__ == "__main__":
    NestedConditionalFlow9()

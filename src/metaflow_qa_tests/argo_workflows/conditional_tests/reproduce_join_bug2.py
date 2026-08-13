from metaflow import FlowSpec, step, Config


class JoinBugFlow2(FlowSpec):
    # also covers config bug
    cfg = Config("foobar", default="config.json")

    @step
    def start(self):
        self.route = "a"
        self.next(self.switch_step)

    @step
    def switch_step(self):
        self.next(
            {"a": self.foreach_a, "b": self.branch_b},
            condition="route",
        )

    @step
    def foreach_a(self):
        self.items = [0, 1]
        self.next(self.branch_a, foreach="items")

    @step
    def branch_a(self):
        # Regular static split (NOT conditional).
        # Both sub_a and sub_b must run and both must succeed before sub_join.
        self.next(self.sub_a, self.sub_b)

    @step
    def sub_a(self):
        self.next(self.sub_join)

    @step
    def sub_b(self):
        if self.input == 1:
            raise Exception("The sub_join should never start!")
        self.next(self.sub_join)

    @step
    def sub_join(self, inputs):
        # BUG: Argo receives  depends: sub-a.Succeeded || sub-b.Succeeded
        # Expected:           depends: sub-a.Succeeded && sub-b.Succeeded
        #
        # With || Argo starts sub_join as soon as either sub_a OR sub_b finishes,
        # meaning sub_join may run while the other branch is still in progress.
        self.next(self.join_foreach)

    @step
    def join_foreach(self, inputs):
        self.next(self.shared)

    @step
    def branch_b(self):
        self.next(self.shared)

    @step
    def shared(self):
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    JoinBugFlow2()

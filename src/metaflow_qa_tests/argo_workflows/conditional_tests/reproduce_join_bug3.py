from metaflow import FlowSpec, step, Config


class JoinBugFlow3(FlowSpec):
    # also covers config bug
    cfg = Config("foobar", default="config.json")

    @step
    def start(self):
        self.route = "a"
        self.next(self.switch_step)

    @step
    def switch_step(self):
        self.next(
            {"a": self.branch_a, "b": self.branch_b},
            condition="route",
        )

    @step
    def branch_a(self):
        # Regular static split (NOT conditional).
        # Both sub_a and sub_b must run and both must succeed before sub_join.
        self.next(self.sub_a, self.sub_b, self.sub_c, self.sub_f)

    @step
    def sub_a(self):
        self.a_items = [0, 1]
        self.next(self.foreach_a, foreach="a_items")

    @step
    def foreach_a(self):
        self.next(self.join_foreach_a)

    @step
    def join_foreach_a(self, inputs):
        self.next(self.sub_join)

    @step
    def sub_b(self):
        self.b_items = [0, 1]
        self.next(self.foreach_b, foreach="b_items")

    @step
    def foreach_b(self):
        if self.input == 1:
            raise Exception("The sub_join should never start!")
        self.next(self.join_foreach_b)

    @step
    def join_foreach_b(self, inputs):
        self.next(self.sub_join)

    @step
    def sub_c(self):
        self.choice = "d"
        self.next({"d": self.sub_d, "e": self.sub_e}, condition="choice")

    @step
    def sub_d(self):
        self.next(self.sub_join)

    @step
    def sub_e(self):
        self.next(self.sub_join)

    # -- sub_f
    @step
    def sub_f(self):
        self.choice = "g"
        self.next({"g": self.sub_g, "h": self.sub_h}, condition="choice")

    @step
    def sub_g(self):
        self.next(self.join_gh)

    @step
    def sub_h(self):
        self.next(self.join_gh)

    @step
    def join_gh(self):
        self.next(self.sub_join)

    @step
    def sub_join(self, inputs):
        # BUG: Argo receives  depends: sub-a.Succeeded || sub-b.Succeeded
        # Expected:           depends: sub-a.Succeeded && sub-b.Succeeded
        #
        # With || Argo starts sub_join as soon as either sub_a OR sub_b finishes,
        # meaning sub_join may run while the other branch is still in progress.
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
    JoinBugFlow3()

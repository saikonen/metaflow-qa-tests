from metaflow import FlowSpec, step, Config, Parameter


class JoinBugFlow4(FlowSpec):
    # also covers config bug
    cfg = Config("foobar", default="config.json")

    should_fail = Parameter("should_fail", default=True)

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
        if self.input == 1 and self.should_fail:
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
        self.splits = [0]
        self.next(self.sub_d_foreach, foreach="splits")

    @step
    def sub_d_foreach(self):
        self.next(self.sub_d_join)

    @step
    def sub_d_join(self, inputs):
        self.next(self.sub_join)

    @step
    def sub_e(self):
        self.next(self.sub_join)

    # -- sub_f
    @step
    def sub_f(self):
        self.choice = "g"
        self.next(
            {
                "g": self.sub_g,
                "h": self.pre_sub_h,
                # "k": self.pre_sub_k
            },
            condition="choice",
        )

    @step
    def sub_g(self):
        self.next(self.join_gh)

    @step
    def pre_sub_h(self):
        self.next(self.sub_h)

    @step
    def sub_h(self):
        self.h_choice = "i"
        self.next({"i": self.sub_i, "j": self.sub_j}, condition="h_choice")

    @step
    def sub_i(self):
        self.next(self.sub_join)

    @step
    def sub_j(self):
        self.next(self.sub_join)

    @step
    def join_gh(self):
        self.next(self.sub_join)

    # @step
    # def pre_sub_k(self):
    #     self.next(self.sub_k)

    # @step
    # def sub_k(self):
    #     self.next(self.sub_l, self.sub_m)

    # @step
    # def sub_l(self):
    #     self.next(self.sub_join)

    # @step
    # def sub_m(self):
    #     self.next(self.sub_n, self.sub_o)

    # @step
    # def sub_n(self):
    #     self.next(self.sub_join)

    # @step
    # def sub_o(self):
    #     self.next(self.sub_join)

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
    JoinBugFlow4()

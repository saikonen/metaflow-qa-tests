from metaflow import step, FlowSpec, current, Parameter


class BaseFlow(FlowSpec):

    param_a = Parameter(
        name="param_a",
        default="default value A",
        type=str,
    )

    @step
    def start(self):
        print("Starting 👋")
        print(self.param_a)
        print("current event", current.trigger)
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")

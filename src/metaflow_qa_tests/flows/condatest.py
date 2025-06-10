from metaflow import FlowSpec, step, conda_base


@conda_base(libraries={"pandas": "1.5.2"}, python="3.11")
class CondaFlow(FlowSpec):
    @step
    def start(self):
        print("In start")
        import pandas as pd

        self.next(self.a)

    @step
    def a(self):
        import pandas as pd

        print("Testing pandas")
        dates = pd.date_range("20130101", periods=6)
        print(dates)
        self.next(self.end)

    @step
    def end(self):
        print("In end")


if __name__ == "__main__":
    CondaFlow()

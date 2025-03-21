from metaflow import step, FlowSpec, Parameter, JSONType

class BaseParamsFlow(FlowSpec):

    param_a = Parameter(
        name="param_a",
        default="default value A",
        type=str
    )

    param_b = Parameter(
        name="param-b",
        default=["a", "b"],
        type=JSONType
    )

    param_c = Parameter(
        name="param-c",
        default={"test": 1},
        type=JSONType
    )

    param_d = Parameter(
        name="param-d",
        default=123,
        type=int
    )

    param_e = Parameter(
        name="param-e",
        default=1.23,
        type=float
    )

    # bookkeeping to make testing easier. these match the parameter names.
    param_defaults = {
        "param_a": "default value A",
        "param-b": ["a", "b"],
        "param-c": {"test": 1},
        "param-d": 123,
        "param-e": 1.23
    }

    @step
    def start(self):
        print("Starting 👋")
        # printing out values for debugging
        for k,v in self.param_defaults.items():
            print(f'{k.upper().replace("_", " ").replace("-", " ")}: {getattr(self, k.replace("-", "_"))}')
        
        # check types of parameters
        for k,v in self.param_defaults.items():
            assert type(getattr(self, k.replace("-","_")))==type(v)

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")
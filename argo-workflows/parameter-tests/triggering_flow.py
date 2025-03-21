from metaflow import step, FlowSpec
from payloads import EVENT_NAME, PAYLOADS

class TriggerArgoParamsTest(FlowSpec):
    @step
    def start(self):
        from metaflow.integrations import ArgoEvent
        
        # trigger events
        for idx, pl in enumerate(PAYLOADS):
            ArgoEvent(EVENT_NAME).publish({"payload_index": idx, **pl})
        # ArgoEvent("params_test_event").publish({"param_a": "param-d not supplied", "param-b": "custom payload B", "param-c": None},)
        # ArgoEvent("params_test_event").publish({"param_a": "param-d not supplied", "param-b": "custom payload B", "param-c": None, "param_d": 444},)

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    TriggerArgoParamsTest()
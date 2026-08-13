from metaflow import step, FlowSpec
from payloads import EVENT_NAME, PAYLOADS


class DeployTimeTriggerParams(FlowSpec):
    @step
    def start(self):
        from metaflow.integrations import ArgoEvent

        # trigger events
        for pl in PAYLOADS:
            ArgoEvent(EVENT_NAME).publish(pl)

        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    DeployTimeTriggerParams()

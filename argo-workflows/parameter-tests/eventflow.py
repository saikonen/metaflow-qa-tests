from baseflow import BaseParamsFlow
from metaflow import trigger, step, Parameter
from payloads import EVENT_NAME, PAYLOADS


@trigger(event=EVENT_NAME)
class EventParamFlow(BaseParamsFlow):
    payload_index = Parameter(name="payload_index", default=None, type=int)

    @step
    def end(self):
        # we do some validation on the parameter values against known payloads and default values
        # just to be sure things are working as expected.
        print("Payload index is: %s" % self.payload_index)
        if self.payload_index is None:
            raise Exception(
                "payload index not provided, not possible to assert parameter validity."
            )

        params_dict = {
            k: getattr(self, k.replace("-", "_")) for k in self.param_defaults.keys()
        }
        print("Testing event against known payloads")
        pl = PAYLOADS[self.payload_index]  # pylint: disable=invalid-sequence-index

        for k, v in params_dict.items():
            if k in pl:
                # param value needs to be from payload if provided
                assert v == pl[k]
            else:
                # param value should be default
                assert v == self.param_defaults[k]


if __name__ == "__main__":
    EventParamFlow()

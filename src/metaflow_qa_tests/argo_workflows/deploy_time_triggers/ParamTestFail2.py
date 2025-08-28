from metaflow import trigger

from payloads import EVENT_NAME
from baseflow import BaseFlow


def params_func(ctx):
    return "param_a"


@trigger(event={"name": EVENT_NAME, "parameters": [params_func]})
class DeployTimeTriggerFail2(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerFail2()

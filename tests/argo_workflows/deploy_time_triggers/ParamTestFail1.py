from metaflow import trigger

from payloads import EVENT_NAME
from baseflow import BaseFlow


def params_func(ctx):
    return "param_a"


@trigger(event={"name": EVENT_NAME, "parameters": {"param_a": params_func}})
class DeployTimeTriggerFail1(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerFail1()

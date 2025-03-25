from metaflow import trigger

from payloads import EVENT_NAME
from baseflow import BaseFlow


def event_dict_func(ctx):
    return {"name": EVENT_NAME, "parameters": ["param_a"]}


@trigger(event=event_dict_func)
class DeployTimeTriggerFlow6(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerFlow6()

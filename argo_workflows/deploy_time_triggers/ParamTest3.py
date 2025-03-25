from metaflow import trigger

from payloads import EVENT_NAME
from baseflow import BaseFlow


def event_name_func(ctx):
    return EVENT_NAME


@trigger(event={"name": event_name_func, "parameters": ["param_a"]})
class DeployTimeTriggerFlow3(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerFlow3()

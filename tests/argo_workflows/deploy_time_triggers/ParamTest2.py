from metaflow import trigger

from payloads import EVENT_NAME
from baseflow import BaseFlow


def event_name_func(ctx):
    return EVENT_NAME


@trigger(event=event_name_func)
class DeployTimeTriggerFlow2(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerFlow2()

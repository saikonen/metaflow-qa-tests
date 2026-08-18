from metaflow import trigger

from payloads import EVENT_NAME
from baseflow import BaseFlow


def event_names_func(ctx):
    return [EVENT_NAME]


@trigger(events=event_names_func)
class DeployTimeTriggerFlow1(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerFlow1()

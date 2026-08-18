from metaflow import trigger

from payloads import EVENT_NAME
from baseflow import BaseFlow


def events_dicts_func(ctx):
    return [{"name": EVENT_NAME, "parameters": ["param_a"]}]


@trigger(events=events_dicts_func)
class DeployTimeTriggerFlow7(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerFlow7()

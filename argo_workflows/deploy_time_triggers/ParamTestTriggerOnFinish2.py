from metaflow import trigger_on_finish
from baseflow import BaseFlow


def flow_names_func(ctx):
    return ["DeployTimeTriggerParams"]


@trigger_on_finish(flows=flow_names_func)
class DeployTimeTriggerOnFinishFlow2(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerOnFinishFlow2()

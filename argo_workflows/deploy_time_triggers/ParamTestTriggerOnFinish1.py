from metaflow import trigger_on_finish

from baseflow import BaseFlow


def flow_name_func(ctx):
    return "DeployTimeTriggerParams"


@trigger_on_finish(flow=flow_name_func)
class DeployTimeTriggerOnFinishFlow1(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerOnFinishFlow1()

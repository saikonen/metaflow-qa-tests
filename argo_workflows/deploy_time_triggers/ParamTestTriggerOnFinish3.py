from metaflow import trigger_on_finish
from baseflow import BaseFlow


def flow_names_dict_func(ctx):
    return [{"name": "DeployTimeTriggerParams"}]


@trigger_on_finish(flows=flow_names_dict_func)
class DeployTimeTriggerOnFinishFlow3(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerOnFinishFlow3()

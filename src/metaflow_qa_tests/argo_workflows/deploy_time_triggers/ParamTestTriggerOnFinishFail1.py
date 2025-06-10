from metaflow import trigger_on_finish
from baseflow import BaseFlow


def flow_name_dict_func(ctx):
    return {"name": "DeployTimeTriggerParams", "project_branch": "test.custombranch"}


@trigger_on_finish(flow=flow_name_dict_func)
class DeployTimeTriggerOnFinishFlowFail1(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerOnFinishFlowFail1()

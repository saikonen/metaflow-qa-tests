from metaflow import trigger_on_finish, project
from baseflow import BaseFlow


def flow_name_dict_func(ctx):
    return {"name": "DeployTimeTriggerParams", "project_branch": "test.custombranch"}


@trigger_on_finish(flow=flow_name_dict_func)
@project(name="deploytime_project")
class DeployTimeTriggerOnFinishFlow6(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerOnFinishFlow6()

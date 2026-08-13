from metaflow import trigger_on_finish, project
from baseflow import BaseFlow


def flow_name_dict_func(ctx):
    return {"name": "DeployTimeTriggerParams", "project": "deploytime_project_two"}


@trigger_on_finish(flow=flow_name_dict_func)
@project(name="deploytime_project")
class DeployTimeTriggerOnFinishFlow5(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerOnFinishFlow5()

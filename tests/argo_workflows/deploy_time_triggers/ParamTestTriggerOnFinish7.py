from metaflow import trigger_on_finish, project
from baseflow import BaseFlow


def flow_name_func(ctx):
    return "DeployTimeTriggerParams"


def project_branch_func(ctx):
    return "test.custombranch"


def project_func(ctx):
    return "another_project"


@trigger_on_finish(
    flow={
        "name": flow_name_func,
        "project": project_func,
        "project_branch": project_branch_func,
    }
)
@project(name="deploytime_project")
class DeployTimeTriggerOnFinishFlow7(BaseFlow):
    pass


if __name__ == "__main__":
    DeployTimeTriggerOnFinishFlow7()

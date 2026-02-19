from baseflow import BaseParamsFlow
from metaflow import Parameter


class NotAllowedParamFlow(BaseParamsFlow):
    script = Parameter("script")


if __name__ == "__main__":
    NotAllowedParamFlow()

import yaml


def read_parameter_file(params_file):

    with open(params_file, "r") as parameters:
        params = yaml.safe_load(parameters)
        return params

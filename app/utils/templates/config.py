import yaml


def load_config(file_path):
    """
    Load YAML configuration from a file.

    :param file_path: Path to the YAML configuration file
    :return: Configuration as a dictionary
    """
    file_path = 'app/'+file_path
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

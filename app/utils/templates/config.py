import yaml
from rich.console import Console

def load_config(file_path):
    """
    Load YAML configuration from a file.

    :param file_path: Path to the YAML configuration file
    :return: Configuration as a dictionary
    """
    console = Console()
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        console.print(f"Error: {str(e)}")
        return None
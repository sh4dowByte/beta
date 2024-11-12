import importlib
import os

from app.config import App

def load_all_script():
    """
    Load all modules from the specified directory and return a list of their names.

    This function recursively walks through the directory tree starting from MODULES_DIR,
    identifies all Python files (excluding __init__.py and example.py), and constructs
    a list of module names by replacing the path separators with dots and removing the
    '.py' extension.

    Returns:
        list: A list containing the names of all modules found.
    """
    base_dir = App.script_path
    template_folder_name = os.path.basename(base_dir)

    modules = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and file != "example.py":
                # Calculate relative path from the root folder
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                # Replace path separator '/' or '\' with '.'
                module_name = relative_path.replace(os.path.sep, '.')[:-3]
                # Add module name to the list

                modules.append({
                    'path': f"app.{template_folder_name}.{module_name}",
                    'name': module_name.split('.')[-1]
                })

    return modules

def load_script(script, options, all = False):
    """
    Load modules based on the provided tags and IDs, check their options, and prepare them for execution.

    This function first loads all available modules and filters them based on the provided tags and IDs.
    It then checks the provided options against the module's metadata, ensuring the options are valid.
    If a module's options are valid, it is added to the list of modules to be returned. Errors encountered
    during the option checks are stored and printed, and the program exits if any errors are found.

    Args:
        tags (str): A comma-separated string of tags to filter modules by.
        id (str): A comma-separated string of IDs to filter modules by.
        options (dict): A dictionary of options to validate against the module's metadata.

    Returns:
        list: A list of dictionaries containing the module's run function, metadata, and default arguments.
    """
    allmodules = load_all_script()

    scripts_set = set(script.split(','))

    if not allmodules:
        return []

    modules = []
    metadatas = []
    for data in allmodules:
        module = importlib.import_module(data['path'])
        metadata = module.metadata
        metadatas.append(metadata)

        if(data['name'] in scripts_set) or all:
            modules.append({
                'run': module.run,
                'metadata': module.metadata,
                'options': options,
                'name': data['name']
            })
    return modules, metadatas

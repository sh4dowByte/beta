import os
import re
import sys
from app.utils.templates import load_config, match
from app.utils.templates.dsl import evaluate_dsl

class MissingRequiredOptionError(Exception):
    """Custom exception for missing required options."""
    pass

def load_all_template(base_dir):
    """
    Load all templates from the specified directory and return a list of their names.

    This function recursively walks through the directory tree starting from TEMPLATES_DIR,
    identifies all YAML files (excluding example.yaml), and constructs
    a list of template names by replacing the path separators.

    Returns:
        list: A list containing the names of all templates found.
    """
    template_folder_name = os.path.basename(base_dir)

    templates = []
    append_template = templates.append
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".yaml") and file != "example.yaml":
                # Calculate relative path from the root folder and replace path separator
                relative_path = os.path.relpath(os.path.join(root, file), base_dir)
                template_name = relative_path.replace(os.path.sep, '/')
                append_template(f"{base_dir}/{template_name}")

    return templates

def load_template(options, base_dir = 'app/data'):
    """
    Load templates based on the provided tags and IDs, check their options, and prepare them for execution.

    This function first loads all available templates and filters them based on the provided tags and IDs.
    It then checks the provided options against the template's metadata, ensuring the options are valid.
    If a template's options are valid, it is added to the list of templates to be returned. Errors encountered
    during the option checks are stored and printed, and the program exits if any errors are found.

    Args:
        tags (str): A comma-separated string of tags to filter templates by.
        id (str): A comma-separated string of IDs to filter templates by.
        options (dict): A dictionary of options to validate against the template's metadata.

    Returns:
        list: A list of dictionaries containing the template's run function, metadata, and default arguments.
    """

    template_names = load_all_template(base_dir)

    templates_found = 0

    if not template_names:
        return []

    templates = []
    metadatas = []
    for template_name in template_names:
        
        config = load_config(template_name)

        if config:
            info = config.get('info', {})
            metadatas.append(info)

            run = replace_placeholders(config, options)
            templates_found += 1
            templates.append({
                'run': run,
                'metadata': config,
            })
    
    return templates, metadatas

def replace_placeholders(obj, variables, root_config=None):
    """
    Function to replace placeholders with values from local variables.
    
    Description:
    The `replace_placeholders` function is designed to recursively replace placeholders
    in a configuration object, such as a dictionary, list, or string, with corresponding 
    values from a given set of variables or configuration options. It supports both 
    standard variable replacements and more complex DSL (Domain-Specific Language) expressions.
    
    This function operates in two main steps:
    1. DSL Evaluation: First, it identifies and evaluates any DSL expressions in the object.
       These expressions, such as generating random strings, are evaluated only once to 
       prevent inconsistent outputs.
    2. Variable Replacement: After DSL evaluation, the function replaces placeholders 
       with corresponding values from `variables` or `root_config`.
    """
    # If root_config is not provided, use obj as the root configuration
    if root_config is None:
        root_config = obj  # Store a reference to the main config

    def evaluate_placeholder(value):
        if isinstance(value, str):
            # Search for DSL placeholders and evaluate them
            def repl(match):
                var_name = match.group(1)
                # Check if the DSL value has been evaluated before
                if var_name in variables:
                    return variables[var_name]

                # Evaluate the DSL expression if found
                if '(' in var_name and ')' in var_name:
                    evaluated_value = evaluate_dsl(var_name)
                    # Store the evaluated DSL result in variables to avoid re-evaluation
                    variables[var_name] = str(evaluated_value)
                    return str(evaluated_value)
                else:
                    # Retrieve from variables or from root_config if available
                    return variables.get(var_name, root_config.get('options', {}).get(var_name, {}).get('default', match.group(0)))
            # Replace the placeholders in the string
            return re.sub(r'\{\{(.*?)\}\}', repl, value)
        elif isinstance(value, list):
            # Recursively evaluate each element in the list
            return [evaluate_placeholder(v) for v in value]
        elif isinstance(value, dict):
            # Recursively evaluate each key-value pair in the dictionary
            return {k: evaluate_placeholder(v) for k, v in value.items()}
        else:
            # Return the value unchanged if it's not a string, list, or dict
            return value

    # Step 1: Evaluate all DSL placeholders in the object
    evaluated_obj = evaluate_placeholder(obj)

    # Step 2: Replace placeholders in the evaluated object
    if isinstance(evaluated_obj, dict):
        result = {k: evaluate_placeholder(v) for k, v in evaluated_obj.items()}
    elif isinstance(evaluated_obj, list):
        result = [evaluate_placeholder(v) for v in evaluated_obj]
    elif isinstance(evaluated_obj, str):
        result = evaluate_placeholder(evaluated_obj)
    else:
        result = evaluated_obj

    error = []
    # Validate that all required options are provided
    if root_config and 'options' in root_config:
        for key, option in root_config['options'].items():
            if option.get('required', False) and key not in variables:
                error.append(f"Required option '{key}' is missing.")

    if error:
        print(f"\nTemplate: {root_config['id']}")
        for err in error:
            print(f"{err}")
        print('\n')
        sys.exit()

    return result

def run_template(config, response = '', ip = '', ):
    result = []
    if config.get('match'):
        result = result + match(config, response)
   
    return result
import os

class App:
    """
    Represents the application configuration and paths.

    Attributes:
        version (str): Current version of the application. Default is '1.0.0'.
        app_dir (str): Absolute path to the directory where the application is located.
        script_path (str): Absolute path to the 'scripts' directory within the application.
        data_path (str): Absolute path to the 'data' directory within the application.
    """
    
    version = '1.0.0'
    app_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(app_dir, 'scripts')
    data_path = os.path.join(app_dir, 'data')

from fastscript import *

@call_parse
def validate_requirements(settings_path: Param("Path to settings.ini in root directory", str)="./settings.ini",
                          requirements_path: Param("Path to requirements.txt file", str)="./requirements.txt",
                          verbose: Param("Level of verbosity", bool)=False):
    """
    Ensures that the requirements found in the root-level settings.ini file match those found in the 
    requirements.txt file.
    """
    with open(settings_path, "r") as f:
        lines = f.readlines()
    settings_reqs = [l.lstrip("requirements = ") for l in lines if l.startswith("requirements = ")][0].split(" ")
    
    with open(requirements_path, "w") as f:
        f.write("\n".join(settings_reqs))
    
    if verbose:
        print(f"Updated the requirements at {requirements_path} with the following: {settings_reqs}.")
    
    
    

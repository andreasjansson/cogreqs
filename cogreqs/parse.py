from typing import Dict


def find_pip_package_version_hints(folder: str) -> Dict[str, str]:
    """
    Based on the contents of the repository folder, look for
    hints for Python package versions. For example, look for
    requirements.txt, Conda's environment.yml, and versions
    written out in the body of README.md.
    """
    # TODO: implement this
    return {}


def find_python_version(folder: str) -> str:
    """
    Based on the contents of the repository folder, look for
    specific Python veresion requirements. For example, look
    in Conda's environment.yml, README.md ,etc.
    """
    # TODO: implement this
    return "3.8"

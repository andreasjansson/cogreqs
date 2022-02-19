from typing import Dict, List
import sys
import os
import argparse
import logging
from pipreqs import pipreqs
import yarg

from .types import Config, Build, PythonPackage
from .exceptions import CogreqsException
from .heuristics import apply_heuristics
from .parse import find_pip_package_version_hints, find_python_version
from .mappings import apply_additional_package_mappings
from .predict_template import predict_template


def fetch_pip_version(package_name: str) -> str:
    """
    Fetch and return the latest release version from PyPI,
    or return "error-fetching-release" if there was an error
    (e.g. the package doesn't exist).
    """
    try:
        pkg = yarg.get(package_name)
        return pkg.latest_release_id
    except Exception as e:
        logging.debug(e)
        return "error-fetching-release"


def get_pip_versions(
    package_names: List[str], version_hints: Dict[str, str]
) -> List[PythonPackage]:
    """
    Given a list of package names, return PythonPackages with
    names and versions. Versions come from either the
    provided "package hints", or directly from PyPI.
    """
    packages = []
    for name in package_names:
        if name in version_hints:
            version = version_hints[name]
        else:
            version = fetch_pip_version(name)
        packages.append(PythonPackage(name, version))
    return packages


def python_packages_from_repo(folder: str) -> List[PythonPackage]:
    """
    Given a repository folder, return a list of versioned python
    packages.
    """
    version_hints = find_pip_package_version_hints(folder)
    import_names = pipreqs.get_all_imports(path=folder, encoding="utf-8-sig")
    package_names = pipreqs.get_pkg_names(import_names)
    package_names = apply_additional_package_mappings(package_names)
    packages_with_versions = get_pip_versions(package_names, version_hints)
    return packages_with_versions


def config_from_repo(folder: str, use_gpu: bool) -> Config:
    """
    Given a repository folder, return a Cog config object
    that can be serialized to cog.yaml.
    """
    python_version = find_python_version(folder)
    python_packages = python_packages_from_repo(folder)

    config = Config(
        build=Build(
            gpu=use_gpu,
            python_version=python_version,
            python_packages=python_packages,
            system_packages=set(),
            run=[],
            cuda=None,
            cudnn=None,
            python_extra_index_urls=[],
            python_find_links=[],
        ),
        image=None,
        predict=None,
    )

    config = apply_heuristics(config)

    return config


def generate_files(
    folder: str,
    force_overwrite: bool,
    use_gpu: bool,
    config_path: str,
    predict_path: str,
):
    """
    Given a repository folder, construct and write cog.yaml and
    predict.py to the file system (or stdout if config_path/predict_path
    is "-", or not at all if config_path/predict_path is "/dev/null").
    """
    if config_path not in ("-", "/dev/null"):
        if os.path.exists(config_path):
            if force_overwrite:
                print(f"Overwriting {config_path}")
            else:
                raise CogreqsException(
                    f"{config_path} already exists, exiting. Use --force-overwrite to overwrite it"
                )
        else:
            print(f"Writing {config_path}")

    config = config_from_repo(folder=folder, use_gpu=use_gpu)
    if config_path == "-":
        if predict_path == "-":
            print("#### cog.yaml")
            print()
        print(config.to_yaml_string())
    elif config_path != "/dev/null":
        if not os.path.isabs(config_path):
            config_path = os.path.join(folder, config_path)
        with open(config_path, "w") as f:
            f.write(config.to_yaml_string())

    if predict_path not in ("-", "/dev/null"):
        if os.path.exists(predict_path):
            if force_overwrite:
                print(f"Overwriting {predict_path}")
            else:
                raise CogreqsException(
                    f"{predict_path} already exists, exiting. Use --force-overwrite to overwrite it"
                )
        else:
            print(f"Writing {predict_path}")

    if predict_path == "-":
        if config_path == "-":
            print()
            print("#### predict.py")
            print()
        print(predict_template)
    elif predict_path != "/dev/null":
        if not os.path.isabs(predict_path):
            predict_path = os.path.join(folder, predict_path)
        with open(predict_path, "w") as f:
            f.write(predict_template)


def main():
    parser = argparse.ArgumentParser(
        description="""Generate cog.yaml and predict.py from an existing repository.

This is an experimental alternative to cog init"""
    )
    parser.add_argument(
        "-f",
        "--force-overwrite",
        action="store_true",
        help="Overwrite existing cog.yaml and predict.py",
    )
    parser.add_argument("-g", "--gpu", action="store_true", help="Use GPU")
    parser.add_argument(
        "--config-path", default="cog.yaml", help="Config file path (default cog.yaml). --config-path=- will write to stdout, --config-path=/dev/null surpresses config file output"
    )
    parser.add_argument(
        "--predict-path",
        default="predict.py",
        help="Predict file path (default predict.py). --predict-path=- will write to stdout, --predict-path=/dev/null surpresses predict file output",
    )
    parser.add_argument("folder", help="Project folder")
    args = parser.parse_args()

    try:
        generate_files(
            folder=args.folder,
            force_overwrite=args.force_overwrite,
            use_gpu=args.gpu,
            config_path=args.config_path,
            predict_path=args.predict_path,
        )
    except CogreqsException as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

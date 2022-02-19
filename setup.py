from pathlib import Path
from setuptools import setup, find_packages

cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name="cogreqs",
    description="Automatically construct cog.yaml from a repository",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.0.5",
    packages=find_packages(exclude=["test", "*.test", "*.test.*"]),
    entry_points={
        "console_scripts": [
            "cogreqs = cogreqs.cogreqs:main",
        ],
    },
    include_package_data=True,
    install_requires=[
        "pipreqs~=0.4.11",
        "yarg~=0.1.9",
        "dacite~=1.6.0",
        "ruamel.yaml~=0.17.21",
    ],
)

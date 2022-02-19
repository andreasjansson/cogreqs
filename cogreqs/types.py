from __future__ import annotations
from io import StringIO
from typing import List, Optional, Set
from dataclasses import dataclass
import dacite
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


@dataclass
class PythonPackage:
    name: str
    version: Optional[str]

    def __str__(self):
        if self.version is not None:
            return f"{self.name}=={self.version}"
        return self.name


@dataclass
class Build:
    gpu: bool
    python_version: str
    python_extra_index_urls: List[str]
    python_find_links: List[str]
    python_packages: List[PythonPackage]
    run: List[str]
    system_packages: Set[str]
    cuda: Optional[str]
    cudnn: Optional[str]

    def to_yaml_dict(self):
        """
        Deserialize to ruamel.yaml dict-like object, possibly
        annotated with comments.
        """
        yaml = YAML()
        yaml.preserve_quotes = True
        d = yaml.load("{}")

        d["gpu"] = self.gpu
        d.yaml_set_comment_before_after_key(
            "gpu", "set to true if your model requires a GPU", indent=2
        )

        d["system_packages"] = list(sorted(self.system_packages))
        d.yaml_set_comment_before_after_key(
            "system_packages",
            """
a list of ubuntu apt packages to install
""",
            indent=2,
        )

        d["python_version"] = self.python_version
        d.yaml_set_comment_before_after_key(
            "python_version",
            """
python version in the form '3.8' or '3.8.12'
""",
            indent=2,
        )

        d["python_packages"] = [str(p) for p in self.python_packages]
        d.yaml_set_comment_before_after_key(
            "python_packages",
            """
a list of packages in the format <package-name>==<version>
""",
            indent=2,
        )

        if self.python_extra_index_urls:
            d["python_extra_index_urls"] = self.python_extra_index_urls
        if self.python_find_links:
            d["python_find_links"] = self.python_find_links

        d["run"] = self.run
        d.yaml_set_comment_before_after_key(
            "run",
            """
commands run after the environment is setup
""",
            indent=2,
        )
        if self.cuda:
            d["cuda"] = self.cuda
        if self.cudnn:
            d["cudnn"] = self.cudnn
        for k, v in d.items():
            d[k] = double_quote(v)
        return d


@dataclass
class Config:
    build: Build
    image: Optional[str]
    predict: Optional[str]

    @staticmethod
    def from_yaml(s: str) -> Config:
        """
        Load a YAML string as a Config object.
        """
        yaml = YAML(typ="safe")
        data = yaml.load(s)
        return dacite.from_dict(data_class=Config, data=data)

    def to_yaml_dict(self):
        """
        Deserialize to ruamel.yaml dict-like object, possibly
        annotated with comments.
        """
        d = YAML().load("{}")
        d["build"] = self.build.to_yaml_dict()
        d.yaml_set_comment_before_after_key(
            "build",
            """Configuration for Cog ⚙
Reference: https://github.com/replicate/cog/blob/main/docs/yaml.md

""",
        )
        if self.image is not None:
            d["image"] = DoubleQuotedScalarString(self.image)
        if self.predict is not None:
            d["predict"] = self.predict
        return d

    def to_yaml_string(self) -> str:
        """
        Deserialize as a YAML string.
        """
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.representer.add_representer(list, list_representer)
        s = StringIO()
        yaml.dump(self.to_yaml_dict(), s)
        return s.getvalue()


def double_quote(x):
    """
    Ensure that the YAML representation of x is double
    quoted, if x is a string.
    """
    if isinstance(x, str):
        return DoubleQuotedScalarString(x)
    if isinstance(x, list):
        return [double_quote(s) for s in x]
    return x


def list_representer(representer, data):
    """
    Ensure that empty lists are represented as empty strings
    rather than [].
    """
    if len(data) == 0:
        return representer.represent_scalar('tag:yaml.org,2002:null', "")
    return representer.represent_sequence('tag:yaml.org,2002:seq', data)

import os

from setuptools import setup, find_packages
from setuptools.command.install import install
from functools import reduce


class PostInstall(install):
    def __init__(self, *args, **kwargs):
        super(PostInstall, self).__init__(*args, **kwargs)
        _install_requirements()


def _install_requirements():
    os.system("pre-commit install")


REQUIRED_PACKAGES = [
    "pydantic == 1.10.2",
    "black == 22.8.0",
    "pytest-mock == 3.8.2",
    "httpx == 0.23.3",
    "tenacity == 8.0.1",
]

EXTRA_REQUIREMENTS = {}

name = "skip-common-lib"
version = "1.0.0"
description = "A modular library that exposes a set of common operations"

setup(
    name=name,
    version=version,
    description=description,
    python_requires=">=3.9",
    packages=[],  # ["res", *find_packages(include=["hemunah_core*"])],
    package_data={"": ["res/*.csv", "res/*.json", "res/*.yaml"]},
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
    extras_require={
        **EXTRA_REQUIREMENTS,
        "all": reduce(lambda agg, value: agg + value, EXTRA_REQUIREMENTS.values(), []),
    },
    cmdclass={"install": PostInstall},
)

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
    "fastapi == 0.87.0",
    "uvicorn[standard] == 0.20.0",
    "pymongo == 4.3.2",
    "motor == 3.1.1",
    "pydantic == 1.10.2",
    "redis == 4.3.4",
    "asyncio-redis == 0.16.0" "black == 22.8.0",
    "pytest-mock == 3.8.2",
    "firebase-admin == 6.0.1",
    "python-dotenv == 0.21.0",
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

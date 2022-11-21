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
    "Flask-PyMongo == 2.3.0",
    "pymongo == 4.3.2",
    "Flask-APScheduler == 1.12.4",
    "Flask-JWT-Extended == 4.4.4",
    "PyJWT == 2.6.0",
    "pydantic == 1.10.2",
    "redis == 4.3.4",
    "black == 22.8.0",
    "pytest-mock == 3.8.2",
    "firebase-admin == 6.0.1",
]

EXTRA_REQUIREMENTS = {}

name = "skip-common-lib"
version = "1.0.0"
description = "A modular library that exposes a set of database operation"

setup(
    name=name,
    version=version,
    description=description,
    python_requires=">=3.8",
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

import json

from inspect import getsourcefile
from os.path import abspath
from pathlib import Path
from typing import Any


class Resource:
    @classmethod
    def get_test_resources_folder_path(cls) -> Path:
        source_file_path = abspath(getsourcefile(lambda: 0))
        res_directory_path = Path.absolute(
            Path(source_file_path).parents[2] / "tests" / "resources"
        )
        local_res_directory_path = Path.absolute(
            Path(source_file_path).parents[3] / "tests" / "resources"
        )
        if not Path.exists(res_directory_path):
            if Path.exists(local_res_directory_path):
                return local_res_directory_path
            raise ValueError("could not find resource directory")

        return res_directory_path

    @classmethod
    def get_test_resources_file_path(cls, file_name: str) -> str:
        res_file_path = Path(cls.get_test_resources_folder_path() / file_name)
        if not Path.exists(res_file_path):
            raise ValueError("could not find resource file")

        return res_file_path

    @classmethod
    def open_test_resource(cls, file_name: str) -> Any:
        file_path = cls.get_test_resources_file_path(file_name)
        with open(file_path, "r") as f:
            return json.loads(f.read())

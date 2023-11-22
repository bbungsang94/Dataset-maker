import copy
import os
from typing import Dict, Any, Union

from utilities.io import load_yaml


class ModelPath:
    def __init__(self, root: str, filename: str,
                 config: str = None, extension: str = None, check_sanity=True):
        if '.' in filename:
            stub = filename.split('.')
            filename = ".".join(stub[:-1])
            extension = stub[-1]
        else:
            if extension is None:
                raise "[Arguments] Not matched filename without extension and extension is null."

        self.root = root
        self.filename = filename
        self.extension = extension

        self.config_path = config
        if check_sanity:
            self.config = self.__check_sanity()

    @property
    def full_path(self):
        return os.path.join(self.root, self.filename + '.' + self.extension)

    def get_args(self):
        return {'model_path': self.full_path, 'config': self.config}

    def __check_sanity(self) -> Union[Dict[str, Any], None]:
        if self.root and os.path.isdir(self.root) is False:
            print("[System] Not found directory: " + self.root)
            raise FileNotFoundError
        if not os.path.isfile(self.full_path):
            print("[System] Not found model file(exists directory): " + self.filename + '.' + self.extension)
            raise FileNotFoundError
        if self.config_path:
            if 'yaml' not in self.config_path:
                print("[System] config file can handle .yaml file only.")
                raise TypeError
            return load_yaml(self.config_path)

        return None

    @staticmethod
    def unpack(pack: Dict[str, Dict[str, Any]]):
        release = dict()
        for key, value in pack.items():
            release[key] = ModelPath(**value)
        return release

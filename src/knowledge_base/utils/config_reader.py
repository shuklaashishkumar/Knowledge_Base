
import yaml 
from knowledge_base.utils import constants 
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Literal



class ConfigReader:
    def __init__(self, path: str):
      
        self.path = path
        self._setup()

    def _setup(self):

        with open(self.path, "r") as f:
            self.config = yaml.safe_load(f)

    def __getitem__(self, key):
        return self.config[key]

    
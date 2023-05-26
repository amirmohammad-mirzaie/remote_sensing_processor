from pathlib import Path
import os
from dotenv import dotenv_values

def get_base_dir():
    return Path(__file__).resolve().parent.parent


_config = {}

for c in ['.env.personal', '.env.develop', '.env.prod']:
    config_dict = dotenv_values(os.path.join(get_base_dir(), 'envs', c),
                                verbose=True)

    a = os.path.join(get_base_dir(), 'envs', c)

    _config.update(**config_dict)

def get_env_config() -> dict:
    return _config

def get_debug() -> bool:
    return bool(int(_config.get('DEBUG')))

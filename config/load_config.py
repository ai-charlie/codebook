import toml
from pathlib import Path
import argparse
import importlib
import json
from easydict import EasyDict as edict

def load_config_from_toml():
    top_path = Path(__file__).parent
    cfg = toml.load(top_path / 'config.toml')
    # print(cfg['face']['img_width'], cfg['service']['port'])
    return cfg


def load_config_from_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg-name1','-a', default='111', help='help messages')
    args = parser.parse_args()
    # print(args.arg_name1)
    return args

    
def load_config_from_pyfile():
    config_file = 'cfg/config.py'
    assert config_file.startswith('cfg/'), 'config file setting must start with cfg/'
    temp_config_name = Path(config_file).name
    temp_module_name = Path(temp_config_name).suffix[0]
    config = importlib.import_module("cfg.base")
    cfg = config.config
    config = importlib.import_module("cfg.%s" % temp_module_name)
    job_cfg = config.config
    cfg.update(job_cfg)
    # print(cfg.port)
    return cfg

    
def load_config_from_json():
    top_path = Path(__file__).parent
    config_file = top_path / 'config.json'
    with open(config_file, "r")as f:
        cfg = json.load(f)
    cfg = edict(cfg)
    # print(cfg.network)
    return cfg


if __name__ == "__main__":
    load_config_from_json()
    load_config_from_argparse()
    load_config_from_pyfile()
    load_config_from_toml()
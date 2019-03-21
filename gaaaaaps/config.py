# -*- coding: utf-8 -*-
import os
import json
from copy import deepcopy

DEFAULT_CONFIG = {
    "sds_dir": "/sds",
    "data_dir": "/data",
    "available_year": ["2018"],
    "white_list": None
}

www_config = None


def get_www_config():
    global www_config
    if www_config is None:
        config_filepath = os.getenv("GAPS_CONFIG")
        www_config = load_config(config_filepath)
    return www_config


def load_config(config_file):
    """
    load config file
    """
    config = json.load(open(config_file, 'r'))
    result = deepcopy(DEFAULT_CONFIG)
    result.update(config)
    return result

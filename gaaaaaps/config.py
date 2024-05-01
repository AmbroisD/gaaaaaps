# -*- coding: utf-8 -*-
import os
import json
from copy import deepcopy

DEFAULT_CONFIG = {
    "sds_dir": "/SDS", # /Users/ambrois/Documents/01_Scripts/data/
    "data_dir": "/SQS", #/Users/ambrois/Documents/01_Scripts/data
    "available_year": ["2021"],
    "white_list": None
}

www_config = None


def get_www_config():
    global www_config
    if www_config is None:
        config_filepath = os.getenv("GAPS_CONFIG")
        www_config = load_config()
    return www_config


def load_config():
    """
    load config file
    """
    result = deepcopy(DEFAULT_CONFIG)
    return result

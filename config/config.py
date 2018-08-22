#!/usr/bin/python
# -*- coding: utf-8 -*-

PATH_DATA_FILE = "%s/%s/%s/global_json/sds_global.json"  # dir, projet, year, year
PATH_INFO_FILE = "%s/%s/%s" # dir, projet, year
# /hawat1/checksds/alparray/2016/2016-sds.json
SDS_DIR = ""
YEAR_AVAILABLE = ["2016", "2017"]

DIR_DATA = "/u/moana/user/ambrois/utopia/sds/"

PROJET = 'ecuador'

STATION_WHITE_LIST = {"enable": True,
                      "station" :["AGOS", "LOJ1", "APED", "EC12", "AAT1", "ARIO", "BOSC", "EC06"]}

#FILTER = {
#    "filter_criteria": {"enable": False,
#                        "comp" : ["Z"],
#                        "loc" : ["00", "", "01", "1", "02", "10"],
#                        "net" : ["XE", "EC", "8G", "IU"],
#                        "type" : ["EH", "HN", "HH", "LH", "SH", "EN", "CH"]},
#
#
#}

#!/usr/bin/python
# -*- coding: utf-8 -*-

PATH_DATA_FILE = "%s/%s/global_json/sds_global.json"  # dir, projet, year, year
PATH_INFO_FILE = "%s/%s" # dir, projet, year
# /hawat1/checksds/alparray/2016/2016-sds.json
SDS_DIR = "/u/pic/sismo-rtdata/archive"

YEAR_AVAILABLE = ["2016"]

DIR_DATA = "/u/moana/user/ambrois/utopia/sds/ecuador"

PROJET = 'ecuador'

STATION_WHITE_LIST = {"enable": False,
                      "station" :["A196A", "A194A", "A199A", "A200A", "A201A",
                                  "A202A", "A204A", "A205A", "A206A", "A208A",
                                  "A209A", "A216A", "A217A", "A209B","ENAUX",
                                  "TRIGF", "MORSI", "FLAF", "CLAF"]}


MODE = 'admin'

#FILTER = {
#    "filter_criteria": {"enable": False,
#                        "comp" : ["Z"],
#                        "loc" : ["00", "", "01", "1", "02", "10"],
#                        "net" : ["XE", "EC", "8G", "IU"],
#                        "type" : ["EH", "HN", "HH", "LH", "SH", "EN", "CH"]},
#
#
#}

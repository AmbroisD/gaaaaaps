#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json
from datetime import datetime, timedelta
#from obspy import UTCdatetime

def load_json(json_file):
    """
    """
    json_data = json.load(open(json_file, 'r'))
    return json_data


def save_json(dict, json_file_name):
    with open(json_file_name, 'w') as outfile:
        json.dump(dict, outfile, indent=2)


def get_resume_json(json_file):
    sys.stderr.write(json_file + '\n')
    json_data = load_json(json_file)
    list_day = []
    info = {}
    for current_x in json_data:
        list_day.append(current_x)
    sort_list_day = sorted(list_day)
    for day in sort_list_day:
        total_gap = 0
        date = datetime.strptime(day, '%Y.%j')
        #if [] not in json_data[day].keys():
        #    print json_data[day]
        #    exit(1)
        gaps = json_data[day]["Gap"]["PeriodList"]
        nb_gaps = len(json_data[day]["Gap"]["PeriodList"])


        for current_gap in gaps:
            end = datetime.strptime(current_gap['EndTime'][:19], '%Y-%m-%dT%H:%M:%S')
            start = datetime.strptime(current_gap['StartTime'][:19], '%Y-%m-%dT%H:%M:%S')
            if end == (date + timedelta(days=1, minutes=1)):
                end = date + timedelta(days=1)
                if start >= end:
                    nb_gaps = nb_gaps - 1
                    continue
            total_gap = total_gap + (end - start).seconds
        info[day] = {'nb_gap': nb_gaps,
                     'percent': (86400. - total_gap)*100 / 86400,
                     'total_gap': total_gap,
                     'overlap': len(json_data[day]["Overlap"]["PeriodList"])}
        #print ' Gap: %s s / %s' % (total_gap, (86400. - total_gap)*100 / 86400)
        #print 'Overlaps : %s' % len(json_data[day]["Overlap"]["PeriodList"])
        #print 'Nb Gaps : %s' % nb_gaps
    return info

#get_list_station_chan(DIR_SAVE)


def global_scan(resultdir, global_dir):
    list_json = os.listdir(resultdir)
    sds_info = {}
    for json_file in list_json:
        if os.path.isfile(os.path.join(resultdir, json_file)):
            info = get_resume_json(os.path.join(resultdir, json_file))
            sds_info[json_file[:-5]] = info
    save_json(sds_info, os.path.join(global_dir, 'sds_global.json'))
    #get_list_station_chan(DIR_SAVE)

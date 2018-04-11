#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
from datetime import datetime
from flask import Response


PATH_DATA_FILE = "%s/%s/%s/%s-sds.json"  # dir, projet, year, year
# /hawat1/checksds/alparray/2016/2016-sds.json

CURRENT_PATH = '/u/moana/user/ambrois/scripts/gaaaaaps/config'


def load_config(config_file):
    """
    load config file
    """
    config = json.load(open(config_file, 'r'))
    dir_data = config['dir_data']
    sds_available = config['sds']
    return dir_data, sds_available


DIR_DATA, SDS_AVAILABLE = load_config(os.path.join(CURRENT_PATH, "config.json"))


def load_json(json_file):
    """
    sds_info['dict_info_station'] = {'net.station': 'jday':[% , gaps]}

    """
    sds_info = json.load(open(json_file, 'r'))
    return sds_info


def error_response(message):
    response = {
        'status': 'error',
        'message': '%s' % message
    }
    return Response(json.dumps(response,
                               separators=(',', ':'),
                               indent=2),
                    mimetype='application/json')


def ok_response(result=None):
    response = {
        'status': 'ok'
    }
    if result is not None:
        response['result'] = result
    return Response(json.dumps(response,
                               separators=(',', ':')),
                    mimetype='application/json')


def get_name_date(days, year):
    """
    return the names of the date
    """
    name_days = []
    for day in days:
        name_days.append(datetime.strptime('%s.%s' % (year, day), '%Y.%j').strftime('%d %b %Y'))
    return name_days


def get_data_for_html_page(start, end, sds_info, year):
    """
    return info data
    """
    days = ['%03d' % x for x in range(start, end+1)]
    days_names = get_name_date(days, year)
    list_cha = sds_info.keys()
    stations = []
    html_sds = {}
    for current_cha in list_cha:
        net, sta, loc, cha = current_cha.split('.')
        stations.append(sta)
        key = '.'.join([sta, loc, cha])
        html_sds[key] = {'net': net}
        avg = 0
        for day in days:
            if day in sds_info[current_cha].keys():
                html_sds[key][day] = {'percent': round((float(sds_info[current_cha][day][0])*100), 2),
                                      'gaps': sds_info[current_cha][day][1],
                                      'color': get_html_color_tab(sds_info[current_cha][day][0]),
                                      'date': datetime.strptime('%s.%s' % (year, day), '%Y.%j').strftime('%d %b %Y'),
                                      'comment': get_comment(current_cha, day, year)}
                avg += (float(sds_info[current_cha][day][0])*100)
            else:
                html_sds[key][day] = {'percent': 0,
                                      'gaps': 0,
                                      'color': 'no_data'}
        html_sds[key]['avg'] = round(float(avg/len(days)), 2)
    return days_names, days, stations, html_sds


def get_html_color_tab(percent):
    percent = percent * 100
    alpha = 0.8
    if percent >= 100.01:
        color = 'pover'
        legend = 'overlap'
    elif percent >= 99.99:
        color = 'p100'
        legend = '100 %'
    elif percent >= 99:
        color = 'p99-100'
        alpha = 1
        legend = '99% - 100%'
    elif percent >= 90:
        color = 'p90-99'
        legend = '90% - 99%'
    elif percent >= 75:
        color = 'p75-90'
        alpha = 1
        legend = '75% - 90%'
    elif percent >= 50:
        color = 'p50-75'
        legend = '50% - 75%'
    elif percent >= 25:
        color = 'p25-50'
        legend = '25% - 50%'
    elif percent > 0:
        color = 'p0-25'
        legend = '0% - 25%'
    elif percent == 0:
        color = 'no_data'
        legend = 'No data'
    return color


def get_sds_info(sds, year):
    """
    return json object
    """
    return load_json(PATH_DATA_FILE % (DIR_DATA, sds, year, year))


def sds_filter(stations, sds_info_data, sta, net):
    """
    return list filtered
    """
    new_stations = []
    if net is None:
        new_sds_info_data = sds_info_data
    else:

        new_sds_info_data = {}
        new_net = net.split(',')
        for key in sds_info_data:
            if sds_info_data[key]['net'] in new_net:
                new_stations.append(key)
                new_sds_info_data[key] = sds_info_data[key]
    if sta is None:
        if not len(new_stations):
            new_stations = stations
    else:
        if not len(new_stations):
            new_stations = sta.split(',')
        else:
            new_stations = list(set(new_stations) & set(sta.split(',')))

    return new_stations, new_sds_info_data

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
from datetime import datetime
from flask import Response


PATH_DATA_FILE = "%s/%s/%s/global_json/sds_global.json"  # dir, projet, year, year
PATH_INFO_FILE = "%s/%s/%s" # dir, projet, year
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


def save_json(sds_info, json_file):
    with open(json_file, 'w') as outfile:
        json.dump(sds_info, outfile, indent=2)


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

def ok_response_table(data=None, keys=None):
    response = {
        'status': 'ok'
    }
    if data is not None:
        response['result'] = data
        response['keys'] = keys
    return Response(json.dumps(response,
                               separators=(',', ':')),
                    mimetype='application/json')


def get_name_date_list(days, year):
    """
    return the names of the date
    """
    name_days = []
    for day in days:
        name_days.append(datetime.strptime('%s.%s' % (year, day), '%Y.%j').strftime('%d %b %Y'))
    return name_days


def get_name_date(day, year):
    """
    return the name of the date
    """
    return datetime.strptime('%s.%s' % (year, day), '%Y.%j').strftime('%d %b %Y')

def get_comment(channel, day, year):
    return None

def get_info(detail, sds):
    """8G.EC04..VM2.json """
    json_file = os.path.join(PATH_INFO_FILE % (DIR_DATA,
                                               sds,
                                               detail['day'][1][-4:]),
                             "%s.%s.%s.%s.json" % (detail["network"],
                                                   detail["station"],
                                                   detail["location"],
                                                   detail["cha"]))
    date = detail['day'][0]
    return json.load(open(json_file, 'r'))[date]


def get_station(detail, sds):
    """8G.EC04..VM2.json """
    json_file = os.path.join(PATH_INFO_FILE % (DIR_DATA,
                                               sds,
                                               '2016'),
                             "%s.%s.%s.%s.json" % (detail["network"],
                                                   detail["station"],
                                                   detail["location"],
                                                   detail["cha"]))
    return json.load(open(json_file, 'r'))


def get_data(sds, start, end, filter_option):
    """
    sds : name of sds
    start: list [day, year] exemple : [100, 2016]
    end: list [day, year] exemple : [130, 2016]
    filter_option dict for filter result

    return list with this stucture
    tableData = [{station:def get_info(channel, day, year):
    return None 'AJAC', location:'00', comp:'HH' , date1 , date2},
    ]
    """
    year = start[1]
    days = []
    for x in range(start[0], end[0]+1):
        days.append('%s.%03d' % (year, x))
    sds_info = get_sds_info(sds, year)
    list_cha = sds_info.keys()
    keys = days
    data = [] # init result

    for current_cha in list_cha:
        if get_channel_filtered(current_cha, filter_option):
            net, sta, loc, cha = current_cha.split('.')
            channel = {'network': net,
                       'station': sta,
                       'location': loc,
                       'cha': cha}
            data_days = {}
            avg = 0
            for day in days:
                if day in sds_info[current_cha].keys():
                    channel[day] = {'color': get_html_color_tab(float(sds_info[current_cha][day]['percent'])),
                                    'info':{'percent': round(float(sds_info[current_cha][day]['percent']), 2),
                                            'gaps': sds_info[current_cha][day]['nb_gap'],
                                            'overlap': sds_info[current_cha][day]['overlap'],
                                            'total_gap': sds_info[current_cha][day]['total_gap'],
                                            'date': datetime.strptime('%s' % day, '%Y.%j').strftime('%d %b %Y'),
                                            'comment': get_comment(current_cha, day, year)}}
                    avg += (float(sds_info[current_cha][day]['percent']))

                else:
                    channel[day] = {'color': 'no_data',
                                    'info': {'percent': 0,
                                             'gaps': 0,
                                             'date': datetime.strptime('%s' % day, '%Y.%j').strftime('%d %b %Y'),
                                             'comment': get_comment(current_cha, day, year)}}
            #channel['data_days'] = data_days

            channel['avg'] = round(float(avg/len(days)), 2)

            data.append(channel)
    return data, keys

def get_channel_filtered(channel, filter_option):
    return True
    #net, sta, loc, comp = channel.split('.')
    #if (net == '*' or net in filter_option['networks']) and (sta == '*' or sta in filter_option['stations']) and (loc == '*' or loc in filter_option['locations']) and (comp == '*' or comp in filter_option['components']):
    #    return True
    #else:
    #    return False


def get_html_color_tab(percent):
    alpha = 0.8
    if percent >= 100.01:
        color = 'pover'
        legend = 'overlap'
    elif percent >= 99.99:
        color = 'p100'
        legend = '100 %'
    elif percent >= 99:
        color = 'p99_100'
        alpha = 1
        legend = '99% - 100%'
    elif percent >= 90:
        color = 'p90_99'
        legend = '90% - 99%'
    elif percent >= 75:
        color = 'p75_90'
        alpha = 1
        legend = '75% - 90%'
    elif percent >= 50:
        color = 'p50_75'
        legend = '50% - 75%'
    elif percent >= 25:
        color = 'p25_50'
        legend = '25% - 50%'
    elif percent > 0:
        color = 'p0_25'
        legend = '0% - 25%'
    else :
        color = 'no_data'
        legend = 'No data'
        print percent
    return color


def get_sds_info(sds, year):
    """
    return json object
    """
    return load_json(PATH_DATA_FILE % (DIR_DATA, sds, year))


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


def get_last_modification(path):
    nbs = os.path.getmtime(path)
    return nbs

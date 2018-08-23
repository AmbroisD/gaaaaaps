#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
from utils import load_json, save_json, get_last_modification
from create_global_scan import global_scan
import config

def get_list_data(sds_path, year):
    """List all file in sds"""
    list_data = []
    for current_x in os.walk(os.path.join(sds_path, year)):
        for files in current_x[2]:
            list_data.append([current_x[0], files])
    return list_data


def update_m_type(file_data, dict_m_date, global_dir):
    """Save last modification """
    last_m = get_last_modification(os.path.join(file_data[0],
                                                file_data[1]))
    dict_m_date[file_data[1]] = last_m
    save_json(dict_m_date, os.path.join(global_dir, 'dict_m_date.json'))


def scan_file(file_data, resultdir):
    """To scan file"""
    os.system('./file-analyse -i %s  -o %s.json' % (os.path.join(file_data[0],
                                                                 file_data[1]),
                                                    os.path.join(resultdir,
                                                                 'tmp')))
    if os.path.exists(os.path.join(resultdir, 'tmp.json'):
        tmp_result = load_json(os.path.join(resultdir,
                                            'tmp.json'))
        os.remove(os.path.join(resultdir, 'tmp.json'))
        tmp_result["DataMetrics"]["Avg"] = int(float(tmp_result["DataMetrics"]["Avg"]))
        tmp_result["DataMetrics"]["Stddev"] = int(float(tmp_result["DataMetrics"]["Stddev"]))
        tmp_result["DataMetrics"]["Rms"] = int(float(tmp_result["DataMetrics"]["Rms"]))
        if os.path.exists(os.path.join(resultdir, '%s.json' % file_data[1].split('.D.')[0])):
            station_dict = load_json(os.path.join(resultdir,
                                              '%s.json' % file_data[1].split('.D.')[0]))
            station_dict[file_data[1].split('.D.')[1]] = tmp_result
        else:
            station_dict = {}
            station_dict[file_data[1].split('.D.')[1]] = tmp_result
        save_json(station_dict, '%s.json' % os.path.join(resultdir,
                                                         file_data[1].split('.D.')[0]))


def scan(file_data, dict_m_date, resultdir, year,  global_dir):
    """Scan file and save date of m """
    print('Scan : %s' % file_data[1])
    scan_file(file_data, resultdir)
    update_m_type(file_data, dict_m_date, global_dir)
   # except:
    #    print("error for %s" % file_data[1])


def test_mseed_file(file_input):
    """Test the file """
    if len(file_input.split('.')) != 7:
        return False
    if file_input.split('.')[4] == 'L':
        return False
    if float(file_input.split('.')[-1]) in range(0, 367):
        return True
    else:
        return False


def get_channel_filtered_station(stream):
    flag = False
    if config.STATION_WHITE_LIST["enable"]:
        if stream[1] in config.STATION_WHITE_LIST["station"]:
            flag = True
    else:
        flag = True
    return flag


def scan_sds(sds_path, year, resultdir, global_dir):
    dict_m_date = load_json(os.path.join(global_dir, 'dict_m_date.json'))
    list_file_data = get_list_data(sds_path, year)
    for file_data in list_file_data:
        if test_mseed_file(file_data[1]):
            if file_data[1] in dict_m_date.keys():
                last_m = get_last_modification(os.path.join(file_data[0],
                                                            file_data[1]))
                if dict_m_date[file_data[1]] == last_m:
                    print('already scan')
                    continue
                else:
                    sds_info = scan(file_data, dict_m_date, resultdir, year, global_dir)
            else:
                sds_info = scan(file_data, dict_m_date, resultdir, year, global_dir)
        else:
            print("%s is not mseed file" % file_data[1])
            continue


def main():
    """
    Basic main function.

    -scan all files
    -create json for each station
    -then scan json and calculate percent and gap.
    """
    parser = argparse.ArgumentParser(description='To Scan SDS')

    parser.add_argument('-S', "--sds", help='Set sds dir')
    parser.add_argument('-d', "--resultdir", help='Set result dir')
    parser.add_argument('-y', "--year", help='Set year')
#    parser.add_argument('-u', "--update", action="store_true",
#                        help='to update the scan')
    parser.add_argument('-a', "--auto", action="store_true",
                        help='scan sds and all year in config file')
    args = parser.parse_args()

    if args.auto:
        for year in config.YEAR_AVAILABLE:
            resultdir = os.path.join(config.DIR_DATA, year)
            global_dir = os.path.join(resultdir, 'global_json')
            if not os.path.exists(resultdir):
                os.makedirs(resultdir)
                os.makedirs(global_dir)
                dict_m_date = {}
                save_json(dict_m_date, os.path.join(global_dir, 'dict_m_date.json'))
            scan_sds(config.SDS_DIR, year, resultdir, global_dir)
            global_scan(resultdir, global_dir)
    else:
        resultdir = os.path.join(args.resultdir, args.year)
        if not os.path.exists(resultdir):
            os.makedirs(resultdir)
            global_dir = os.path.join(resultdir, 'global_json')
            os.makedirs(global_dir)
            dict_m_date = {}
            save_json(dict_m_date, os.path.join(global_dir, 'dict_m_date.json'))
        scan_sds(args.sds, args.year, resultdir, global_dir)
        global_scan(resultdir, global_dir)

if __name__ == '__main__':
    main()

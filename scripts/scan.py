#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
from utils import load_json, save_json, get_last_modification


def get_list_data(sds_path, year):
    """List all file in sds"""
    list_data = []
    for current_x in os.walk(os.path.join(sds_path, year)):
        for files in current_x[2]:
            list_data.append([current_x[0], files])
    return list_data


def update_m_type(file_data, dict_m_date, resultdir):
    """Save last modification """
    last_m = get_last_modification(os.path.join(file_data[0],
                                                file_data[1]))
    dict_m_date[file_data[1]] = last_m
    save_json(dict_m_date, os.path.join(resultdir, 'dict_m_date.json'))


def scan_file(file_data, resultdir):
    """To scan file"""
    os.system('./file-analyse -i %s  -o %s.json' % (os.path.join(file_data[0],
                                                                 file_data[1]),
                                                    os.path.join(resultdir,
                                                                 'tmp')))
    tmp_result = load_json(os.path.join(resultdir,
                                        'tmp.json'))
    if os.path.exists(os.path.join(resultdir, '%s.json' % file_data[1].split('.D.')[0])):
        station_dict = load_json(os.path.join(resultdir,
                                              '%s.json' % file_data[1].split('.D.')[0]))
        station_dict[file_data[1].split('.D.')[1]] = tmp_result
    else:
        station_dict = {}
        station_dict[file_data[1].split('.D.')[1]] = tmp_result
    save_json(station_dict,'%s.json' % os.path.join(resultdir,
                                                    file_data[1].split('.D.')[0]))


def scan(file_data, dict_m_date, resultdir, year):
    """Scan file and save date of m """
    print('Scan : %s' % file_data[1])    
    scan_file(file_data, resultdir)
    update_m_type(file_data, dict_m_date, resultdir)
   # except:
    #    print("error for %s" % file_data[1])


def test_mseed_file(file_input):
    """Test the file """
    if not len(file_input.split('.')) == 7:
        return False   
    if float(file_input.split('.')[-1]) in range(0, 367):
        return True
    else: 
        return False


def scan_sds(sds_path, year, resultdir):
    dict_m_date = load_json(os.path.join(resultdir, 'dict_m_date.json'))
    list_file_data = get_list_data(sds_path, year)
    for file_data in list_file_data:
        if test_mseed_file(file_data[1]):
            if file_data[1] in dict_m_date.keys():
                last_m = get_last_modification(os.path.join(file_data[0],
                                                            file_data[1]))
                if dict_m_date[file_data[1]] == last_m:
                    continue
                else:
                    sds_info = scan(file_data, dict_m_date, resultdir, year)
            else:
                sds_info = scan(file_data, dict_m_date, resultdir, year)
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

    parser.add_argument('-S', "--sds", help='Set sds dir',
                        required=True)
    parser.add_argument('-d', "--resultdir", help='Set result dir',
                        required=True)
    parser.add_argument('-y', "--year", help='Set year',
                        required=True)
    parser.add_argument('-u', "--update", action="store_true",
                        help='to update the scan')
    args = parser.parse_args()

    resultdir = os.path.join(args.resultdir, args.year)
        #dict_info_stations = load_json(os.path.join(resultdir, '%s.json' % dict_info_stations))
    if not os.path.exists(resultdir):
        os.makedirs(resultdir)
        dict_m_date = {}
        save_json(dict_m_date, os.path.join(resultdir, 'dict_m_date.json'))
    scan_sds(args.sds, args.year, resultdir)


if __name__ == '__main__':
    main()


# -*- coding: utf-8 -*-
import os
import sys
import json
import traceback
from datetime import datetime
from datetime import timedelta


def load_json(json_filename):
    """
    Load a JSON from a given filename

    json_filename -- The filename to load

    return        -- The JSON loaded from filename
    """
    result = json.load(open(json_filename, 'r'))
    return result


def save_json(json_object, json_filepath):
    """
    Save a JSON object in a given filepath

    json_object   -- The JSON object to save
    json_filepath -- The JSON filepath
    """
    with open(json_filepath, 'w') as outfile:
        json.dump(json_object, outfile)


def get_sds_files(sds_root, year):
    """
    Give the list of files present in a SDS for a given year

    sds_root -- The root of SDS
    year     -- The request year

    return   -- List of file as absolute path
    """
    result = list()
    for root, dirs, files in os.walk(os.path.join(sds_root, year)):
        for current in files:
            result.append(os.path.join(root, current))
    return result


def is_sds_filename(filename):
    """
    Say if a given filename seem to be a file belonging to SDS structure.
    The test is only based on filename structure.

    filename -- The filename

    return   -- True if the filename seem to be belonging to SDS
                and False otherwise
    """
    if len(filename.split('.')) != 7:
        return False
    if filename.split('.')[4] == 'L':
        return False
    if float(filename.split('.')[-1]) in range(0, 367):
        return True
    else:
        return False


class SDSScanner(object):

    def __init__(self, sds_root, result_root, white_list, verbose):
        """
        Initialize this SDSScanner

        sds_root    -- The SDS root directory
        result_root -- The root directory of result
        white_list  -- The station white list
        verbose     -- Verbosity level
        """
        self.__sds_root = sds_root
        self.__result_root = result_root
        self.__white_list = white_list
        self.__verbose = verbose

    def __must_be_processed(self, station_code):
        """
        Say if a station must be processed

        station_code -- The station IRIS code

        return       -- True if the station must be processed and
                        False otherwise
        """
        if self.__white_list is None:
            return True
        if station_code in self.__white_list:
            return True
        return False

    def __init_scan(self, year):
        """
        Verify and initialize directory structure
        and load already processed file informations.

        year -- The processed year
        """
        self.__resultdir = os.path.join(self.__result_root, year)
        self.__globaldir = os.path.join(self.__resultdir, 'global_json')
        if not os.path.exists(self.__resultdir):
            os.makedirs(self.__resultdir)
            os.makedirs(self.__globaldir)
            dict_m_date = {}
            save_json(dict_m_date, os.path.join(self.__globaldir, 'dict_m_date.json'))
        self.__dict_m_date = load_json(os.path.join(self.__globaldir,
                                                    'dict_m_date.json'))

    def __save_file_info(self, filename, file_info):
        """
        Save information associated with a filename.

        filename  -- The filename
        file_info -- The informations associated with this filename
        """
        # FR.SMPL.00.HHZ.D.2019.057
        #
        # stream_code = FR.SMPL.00.HHZ
        # year_and_jday = 2019.057
        stream_code = filename.split('.D.')[0]
        year_and_jday = filename.split('.D.')[1]
        stream_info = {}
        if os.path.exists(os.path.join(self.__resultdir, '%s.json' % stream_code)):
            stream_info = load_json(os.path.join(self.__resultdir, '%s.json' % stream_code))
        stream_info[year_and_jday] = file_info
        save_json(stream_info, '%s.json' % os.path.join(self.__resultdir, stream_code))

    def __update_m_type(self, filepath):
        """
        Update last analyse time for a given filepath

        filepath -- The filepath to update
        """
        last_m = os.path.getmtime(filepath)
        filename = os.path.basename(filepath)
        self.__dict_m_date[filename] = last_m

    def __normalize_gap_overlap(self, file_analyse, year, yday):
        """
        Search for data in the last minute of previous day and the first
        minute of next day. This data is associated with entry yesterday
        and tomorrow.

        file_analyse -- The file analyse result
        """
        file_analyse["yesterday"] = 0
        file_analyse["tomorrow"] = 0
        first_gap = file_analyse["Gap"]["PeriodList"][0]
        last_gap = file_analyse["Gap"]["PeriodList"][-1]
        begin_day = datetime.strptime("%s.%s" % (year, yday), '%Y.%j')
        end_day = datetime.strptime("%s.%s-23:59:59.999999" % (year, yday), '%Y.%j-%H:%M:%S.%f')
        first_gap_start = datetime.strptime(first_gap["StartTime"][:26], '%Y-%m-%dT%H:%M:%S.%f')
        first_gap_end = datetime.strptime(first_gap["EndTime"][:26], '%Y-%m-%dT%H:%M:%S.%f')
        last_gap_start = datetime.strptime(last_gap["StartTime"][:26], '%Y-%m-%dT%H:%M:%S.%f')
        last_gap_end = datetime.strptime(last_gap["EndTime"][:26], '%Y-%m-%dT%H:%M:%S.%f')

        if first_gap_end < begin_day:
            delta = (begin_day - first_gap_end)
            file_analyse["yesterday"] = delta.seconds + delta.microseconds / 1000000.0
            file_analyse["Gap"]["PeriodList"] = file_analyse["Gap"]["PeriodList"][1:]
        elif first_gap_start < begin_day:
            file_analyse["Gap"]["PeriodList"][0] = {
                "StartTime": begin_day.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "EndTime": first_gap_end.strftime("%Y-%m-%dT%H:%M:%S.%f")
            }
        if last_gap_start > end_day:
            delta = (last_gap_start - end_day)
            file_analyse["tomorrow"] = delta.seconds + delta.microseconds / 1000000.0
            file_analyse["Gap"]["PeriodList"] = file_analyse["Gap"]["PeriodList"][:-1]
        elif last_gap_end > end_day:
            file_analyse["Gap"]["PeriodList"][-1] = {
                "StartTime": last_gap_start.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "EndTime": end_day.strftime("%Y-%m-%dT%H:%M:%S.%f")
            }

    def __analyse_file(self, filepath):
        """
        Analyse a given file.

        filepath  -- The file path to scan

        return    -- The analyse result
        """
        filename = os.path.basename(filepath)
        year = filename.split('.')[-2]
        yday = filename.split('.')[-1]
        result_filename = os.path.join(self.__resultdir, 'tmp.json')
        os.system('./file-analyse -i %s -d %d -y %s  -o %s' %
                  (filepath, int(yday), year, result_filename))

        if not os.path.exists(result_filename):
            filename = os.path.basename(filepath)
            if self.__verbose:
                sys.stderr.write("Can't find file-analyse result for %s\n" % filename)
            return None

        result = load_json(result_filename)
        os.remove(result_filename)
        result["DataMetrics"]["Avg"] = int(float(result["DataMetrics"]["Avg"]))
        result["DataMetrics"]["Stddev"] = int(float(result["DataMetrics"]["Stddev"]))
        result["DataMetrics"]["Rms"] = int(float(result["DataMetrics"]["Rms"]))
        return result

    def __scan_one_file(self, filepath):
        """
        Scan one given filepath and update associated informations

        filepath -- The filepath to scan
        """
        filename = os.path.basename(filepath)
        if not is_sds_filename(filename):
            if self.__verbose > 1:
                print("%s is not a valid SDS filename" % filename)
            return

        if not self.__must_be_processed(filename.split('.')[1]):
            if self.__verbose > 1:
                print("%s filtered, not in white list" % filename)
            return

        if filename in self.__dict_m_date.keys():
            last_m = os.path.getmtime(filepath)
            if self.__dict_m_date[filename] == last_m:
                if self.__verbose > 2:
                    print('already scan')
                    return
        if self.__verbose > 1:
            print('Scan : %s' % os.path.basename(filepath))
        file_info = self.__analyse_file(filepath)

        if file_info is None:
            sys.stderr.write("No analyse result for %s\n" %
                             os.path.basename(filepath))
            return
        self.__normalize_gap_overlap(file_info, int(filename.split(".")[-2]),
                                     int(filename.split(".")[-1]))
        filename = os.path.basename(filepath)
        self.__save_file_info(filename, file_info)

    def __consolidate_one_file(self, result_file):
        """
        Create consolidation information for a given analyse result file.

        result_file -- The result file to consolidate

        return      -- Consolidation information with the following form:
        {
            'nb_gap': <nb gaps>,
            'percent': <data prescence percent>,
            'total_gap': <gaps duration>,
            'overlap': <nb overlaps>
        }
        """
        json_data = load_json(result_file)
        list_day = []
        info = {}
        for current_x in json_data:
            list_day.append(current_x)
        sort_list_day = sorted(list_day)
        for day in sort_list_day:
            total_gap = 0
            sys.stderr.write("%s\n" % day)
            date = datetime.strptime(day, '%Y.%j')
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
                         'percent': (86400. - total_gap) * 100 / 86400,
                         'total_gap': total_gap,
                         'overlap': len(json_data[day]["Overlap"]["PeriodList"])}
        return info

    def __consolidate(self):
        """
        Consolidate file analyse result in a global file.
        """
        list_json = os.listdir(self.__resultdir)
        sds_info = {}
        for json_file in list_json:
            if os.path.isfile(os.path.join(self.__resultdir, json_file)):
                try:
                    info = self.__consolidate_one_file(os.path.join(self.__resultdir, json_file))
                except Exception as exception:
                    if self.__verbose > 0:
                        sys.stderr.write("Error during consolidation of %s: %s\n" %
                                         (json_file, exception))
                        traceback.print_exc()
                        continue
                sds_info[json_file[:-5]] = info
        save_json(sds_info, os.path.join(self.__globaldir, 'sds_global.json'))

    def scan_sds(self, year):
        self.__init_scan(year)
        if self.__verbose > 1:
            print("Scan SDS ....")
        list_files = get_sds_files(self.__sds_root, year)
        try:
            for current_filepath in list_files:
                try:
                    if self.__verbose > 2:
                        print("Processing %s..." % os.path.basename(current_filepath))
                    self.__scan_one_file(current_filepath)
                    self.__update_m_type(current_filepath)
                except Exception as exception:
                    if self.__verbose > 0:
                        sys.stderr.write("Error during processing of %s: %s\n" %
                                         (current_filepath, exception))
                        traceback.print_exc()
        finally:
            save_json(self.__dict_m_date, os.path.join(self.__globaldir,
                                                       'dict_m_date.json'))
        self.__consolidate()

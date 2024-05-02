#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import argparse
from gaaaaaps.config import load_config
from sdsscanner.scanner import SDSScanner


def main():
    """
    Basic main function.

    -scan all files
    -create json for each station
    -then scan json and calculate percent and gap.
    """
    parser = argparse.ArgumentParser(description='To Scan SDS')

    parser.add_argument('-c', "--config", default="config.json", help='Set configuration file')
    parser.add_argument('-y', "--year", help='Set year')
    parser.add_argument('-p', '--program', default="file-analyse", help='The path of file-analyze')
    parser.add_argument('-a', "--auto", action="store_true", default=False,
                        help='scan sds and all year in config file')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()

    config = load_config()
    print(config)

    if not args.auto and args.year is None:
        sys.stderr.write("You must specify -a or -y")
        sys.exit(1)

    if args.auto:
        for year in config["available_year"]:
            scanner = SDSScanner(config["sds_dir"], config["data_dir"],
                                 config["white_list"], args.program,
                                 args.verbose)
            scanner.scan_sds(year)
    else:
        scanner = SDSScanner(config["sds_dir"], config["data_dir"],
                             config["white_list"], args.program,
                             args.verbose)
        scanner.scan_sds(args.year)


if __name__ == '__main__':
    main()

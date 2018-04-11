#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import traceback
from flask import Flask, request, render_template, Response, abort
from scripts.utils import get_data_for_html_page
from scripts.utils import get_sds_info
from scripts.utils import sds_filter
from scripts.utils import error_response
from scripts.utils import ok_response

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('app.html')


@app.route('/ws/get_data', methods=["GET"])
def show_table():
    """
    main fonction
    """
    start = request.args.get('start', default=None, type=int)
    end = request.args.get('end', default=None, type=int)
    sds = request.args.get('sds', default=None)
    year = request.args.get('year', default=None)
    net = request.args.get('net', default=None)
    sta = request.args.get('sta', default=None)
    try:
        if sds is not None and start is not None and end is not None:
            sds_info = get_sds_info(sds, year)
            days_names, days, stations, sds_info_data = get_data_for_html_page(start,
                                                                               end,
                                                                               sds_info['dict_info_station'],
                                                                               year)
            stations, sds_info_data = sds_filter(stations, sds_info_data, sta, net)
            ok_response(sds_info_data)

    except Exception as exception:
        return error_response('%s' % traceback.format_exc())


@app.route('/ws/day', methods=['GET'])
def get_image():
    """
    return image
    """
    if ('sds' not in request.args or
            'year' not in request.args or
            'net' not in request.args or
            'sta' not in request.args or
            'day' not in request.args):
        abort(400)
    try:
        img_dir = os.path.join(DIR_DATA,
                               request.args['sds'],
                               request.args['year'], 'IMG')
        start_filename = '%s.%s' % (request.args['net'], request.args['sta'])
        end_filename = '%s.png' % request.args['day']
        img_list = filter(lambda x: x.startswith(start_filename) and
                          x.endswith(end_filename), os.listdir(img_dir))
        if len(img_list) == 0:
            filename = os.path.join('img/no_data.png')
        else:
            filename = os.path.join(img_dir, img_list[0])

        with open(filename, 'r') as current_f:
            img = current_f.read()
        return Response(img, mimetype='image/png')
    except Exception as exception:
        return error_response('%s' % traceback.format_exc())


@app.route('/comment', methods=['GET'])
def set_comment():
    if ('sds' not in request.args or
            'year' not in request.args or
            'net' not in request.args or
            'sta' not in request.args or
            'day' not in request.args):
        abort(400)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50022)

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import traceback
import json
from flask import Flask, request, render_template, Response, abort
from scripts.utils import get_data, get_info, get_station
from scripts.utils import error_response
from scripts.utils import ok_response, ok_response_table

PROJET = 'ecuador'

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('app.html')


@app.route('/ws/get_data', methods=["GET"])
def get_table_data():
    """
    main fonction
    """
    start = request.args.get('start', default=None)
    end = request.args.get('end', default=None)
    sds = request.args.get('sds', default=None)
    net = request.args.get('net', default='*')
    sta = request.args.get('sta', default='*')
    comp = request.args.get('comp', default='*')
    loc = request.args.get('loc', default='*')
    if sds is not None and start is not None and end is not None:
        try:
            data, keys = get_data(sds,
                                  [int(x) for x in start.split(',')],
                                  [int(x) for x in end.split(',')],
                                  filter_option={"stations": sta,
                                                 "networks": net,
                                                 "components": comp,
                                                 "locations": loc})

            return ok_response_table(data=data, keys=keys)
        except Exception as exception:
            return error_response('%s' % traceback.format_exc())
    else:
        abort(400)


@app.route('/ws/day', methods=['POST'])
def get_info_station():
    """
    return info station for one day
    """
    try:
        s_detail = request.data
        detail = json.loads(s_detail)
        info = get_info(detail, PROJET)
        return ok_response(info)
    except Exception as exception:
        return error_response('%s' % traceback.format_exc())


@app.route('/ws/station', methods=['POST'])
def get_statistics_station():
    """
    return info station for the period
    """
    try:
        s_detail = request.data
        detail = json.loads(s_detail)
        info = get_station(detail, PROJET)
        return ok_response(info)
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
    app.run(host='0.0.0.0', port=50022)

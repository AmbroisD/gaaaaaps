#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, Response, abort
import json
import os

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('app.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

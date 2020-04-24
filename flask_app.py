# env FLASK_APP=flask_app.py FLASK_ENV=development flask run
# python flask_app.py
# ibmcloud login --sso -r eu-de
# ibmcloud target --cf
# ibmcloud cf push
# ibmcloud cf apps

from flask import Flask, escape, request, render_template, Response
import importlib
import sys
import requests
import json
import urllib
import os
import pandas as pd
import glob
import random
import io

import sys
#sys.path.append('../')
#lotj_reports = importlib.import_module('XXXXX')

import config

app = Flask(__name__)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


@app.route('/')
def hello():
    ledger_csvfiles = []
    for file in glob.glob(config.cfg["ledgers_path"] + "/*.csv"):
        ledger_csvfiles.append(os.path.basename(file))

    return render_template('hello.html', ledger_csvfiles=ledger_csvfiles)


@app.route('/dashboard_rt')
def dashboard_rt():
    return render_template('dashboard.html')

@app.route('/dashboard/<id>')
def dashboard_id(id: id):
    return render_template('dashboard.html')

@app.route('/dashboard/<id>/raw')
def dashboard_id_raw(id: id):
    csvfile_path = config.cfg["ledgers_path"] + '/' + id 
    df = pd.read_csv(csvfile_path, encoding='utf-8')
    columns_included = df.columns.values
    return render_template('dashboard.html', csvfile_path=csvfile_path,
        tables=[df[columns_included].to_html(classes=['table-striped', 'table-gonance-default'], table_id='ledger-table')], 
        titles=df[columns_included].columns.values)

@app.route('/csvexplorer', methods = ['POST', 'GET'])
def csvexplorer():
    if request.method == 'POST':
        result = request.files

        file = request.files['csvfile']
        df = pd.read_csv(file)

        #columns_included = ['Date', 'Quarter']
        columns_included = df.columns.values
    return render_template('csvexplorer.html', 
        tables=[df[columns_included].to_html(classes=['table-striped', 'table-gonance-default'], table_id='ledger-table')], 
        titles=df[columns_included].columns.values)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
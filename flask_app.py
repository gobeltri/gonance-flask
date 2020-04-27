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
gonance = importlib.import_module('helpers.gonance')

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
    csvfile_path = config.cfg["ledgers_path"] + '/' + id 
    df1 = pd.read_csv(csvfile_path, encoding='utf-8')
    df2 = gonance.normalize_ledger_df(df1)

    investment_df = gonance.figure_by_group_and_period(
        df=df2,
        figure='Investment Gross',
        group='Product',
        period='Quarter')

    value_df = gonance.figure_by_group_and_period(
        df=df2,
        figure='Value',
        group='Product',
        period='Quarter')

    df4 = value_df.join(investment_df, lsuffix='_value', rsuffix='_investment')
    df5 = gonance.enhance_historical(df4)

    df6 = gonance.format_historical(df5)

    columns_included = df4.columns
    columns_included = ['Product', 'Allocation', '20Q2_value', 'Total Investment', 'Delta Last-Y', 'Delta Last-Q', 'Returns', 'Returns %']

    return render_template('dashboard.html',
        tables=[df5[columns_included].to_html(classes=['table-gonance-default'], table_id='ledger-table')], 
        titles=df5.columns.values)

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
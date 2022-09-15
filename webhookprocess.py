import sys
from flask import Flask, jsonify
import os
from flask import send_from_directory

import zipfile
from urllib.request import urlopen,Request
import shutil
import os
import pandas as pd
from csv import DictReader
import re

app = Flask(__name__)

"""
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')
"""
@app.route('/')
@app.route('/homepage')
def home():
    return "Hello World Success changed"

@app.route('/mdrmcsv')
def mdrmcsv():
    url = 'https://www.federalreserve.gov/apps/mdrm/pdf/MDRM.zip'
    file_name = 'MDRM.zip'

    req = Request('https://www.federalreserve.gov/apps/mdrm/pdf/MDRM.zip', headers={'User-Agent': 'Mozilla/5.0'})

    # extracting zipfile from URL
    with urlopen(req) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

        # extracting required file from zipfile
        with zipfile.ZipFile(file_name) as zf:
            zf.extract('MDRM_CSV.csv')

    # deleting the zipfile from the directory
    os.remove('MDRM.zip')

    # loading data from the file
    data = pd.read_csv('MDRM_CSV.csv', skiprows=1)
    data["Name"] = ""

    res = data.columns
    #print(res)

    data.columns.values[0] = "Mnemonic__c"
    data.columns.values[1] = "Item_Code__c"
    data.columns.values[2] = "Start_Date__c"
    data.columns.values[3] = "End_Date__c"
    data.columns.values[5] = "Confidentiality__c"
    data.columns.values[6] = "Item_Type__c"
    data.columns.values[7] = "Reporting_form__c"

    mdrmDataDict = data.to_dict('records')

    count = 0

    # format the data
    for mdrm in mdrmDataDict:

        if mdrm['Name'] == '':
            # print('reporting form',type(mdrm['Reporting_form__c']))
            # print('Mnomonic',type(mdrm['Mnemonic__c']))
            # print('Item code',type(mdrm['Item_Code__c']))
            # print('Name',type(mdrm['Name']))
            mdrm['Name'] = str(mdrm['Reporting_form__c']) + mdrm['Mnemonic__c'] + str(mdrm['Item_Code__c'])

        if mdrm['Description']:
            mdrm['Description'] = re.sub('<[^<]+?>', '', str(mdrm['Description']))
            mdrm['Description'] = mdrm['Description'].replace('&#x0D;', '')
            count += 1
            # print(mdrm['Description'])

    # print(type(d))

    #print(count)

    #print(mdrmDataDict[1])

    return "MDRMCSV Success"


if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run()

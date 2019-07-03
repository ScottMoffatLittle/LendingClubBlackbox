import requests
import configparser
import json
from  bb_module_default import invest_or_not

URL = "http://172.30.18.126:9187/kml/model/blackbox/deployment/23/infer"

MY_PARAMS = ['delinq2Yrs', 'loanAmount', 'annualInc', 'homeOwnership', 'empLength', 'ficoRangeHigh', 'ficoRangeLow',\
             'purpose', 'dti', 'grade']

def get_data():
    API_KEY_FILE = "api.key"
    REQUEST_URL = "https://api.lendingclub.com/api/investor/v1/loans/listing?showAll=True"

    config = configparser.ConfigParser()
    config.read(API_KEY_FILE)
    API_KEY = config["InvestorAPI"]["API_KEY"]

    headers = {
        'Authorization': API_KEY,
        'X-LC-LISTING-VERSION': '1.3',
        'Content-type': 'application/json'
        }

    r = requests.get(REQUEST_URL, headers=headers)

    loanlist = r.json()
    return loanlist

#Pull all live loans from LendingClub website
loanlist = get_data()
ID_list = []
#Format the loans to form that model can accept
loans_json = []
for i in range(len(loanlist['loans'])):
    loan = loanlist['loans'][i]
    ID_list.append(loan['id'])
    loan_payload = {}
    for param in MY_PARAMS:
        loan_payload[param] = loan[param]
    loans_json.append(loan_payload)

#Print the results
i = 0
r = requests.post(url = URL, json = loans_json)
data = r.json()
for loan in data['response']['inference']:
    print('Loan ID: ' + str(ID_list[i]))
    for feature in MY_PARAMS:
        print(feature + ': ' + str(loan[feature]))
    answer = loan['invest']
    if answer == 0: answer = 'No\n'
    else: answer = 'Yes\n'
    print('invest: ' + answer)
    i += 1

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os
import category_encoders as ce
import json
import pickle

FEATURES = ['loan_amnt', 'emp_length', 'home_ownership', 'annual_inc', 'purpose',\
            'dti', 'delinq_2yrs', 'loan_status', 'grade', 'fico_range_low', 'fico_range_high']

model = pickle.load(open('LC_model.sav', 'rb'))
encoder = pickle.load(open('LC_encoder.sav', 'rb'))
    
def conv_emp_len(length):
    if length < 12:
        return '< 1 year'
    elif length > 120:
        return '10+ years'
    else:
        yrs = str(int(length) // 12)
        return yrs + ' years'
    
    
def prepare_new_data(df, endocer):
    df = df[FEATURES]
    
    #Apply the same encoding as before to the new data
    df = encoder.transform(df)
    
    #Drop loan status, as we already know it's current
    df = df.drop('loan_status', axis=1)
    
    #the dataset has NaN values, so replace them using ffill
    df = df.fillna(0)
    
    return df

def prepare_request_data(data_json):

    df = pd.DataFrame.from_dict([data_json], orient='columns')
    df = df.rename(index=str, columns={'delinq2Yrs': 'delinq_2yrs', 'loanAmount': 'loan_amnt',\
                                  'annualInc': 'annual_inc', 'homeOwnership': 'home_ownership',\
                                 'empLength': 'emp_length', 'ficoRangeHigh': 'fico_range_high',\
                                 'ficoRangeLow': 'fico_range_low'})
    df['loan_status'] = 'Current'
    df = df[FEATURES]
    df = df.fillna(0)
    df['emp_length'] = df['emp_length'].apply(conv_emp_len)
    return df

def predict_on_new_data(model, df, encoder):
    X = prepare_new_data(df, encoder)
    y_pred = (model.predict_proba(X)[:,1] >= 0.85).astype(bool)
    return y_pred

def get_loan_features(data):
    loan_features = {}
    for feature in data.columns:
        loan_features[feature] = data[feature][0]

    return loan_features

def invest_or_not(inMap):
    #Format the data to look like the past dataset
    req_data = prepare_request_data(inMap)

    #Predict whether to invest on new loans
    prediction = predict_on_new_data(model, req_data, encoder)
    prediction = int(prediction[0])
    outMap = {'invest': prediction}
    return outMap
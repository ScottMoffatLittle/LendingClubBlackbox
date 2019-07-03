import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os
import category_encoders as ce
import json
import pickle

FEATURES = ['loan_amnt', 'emp_length', 'home_ownership', 'annual_inc', 'purpose',\
            'dti', 'delinq_2yrs', 'loan_status', 'grade', 'fico_range_low', 'fico_range_high']

def read_in_data():
	dataframes = []
	DIR = './data/'
	FILENAMES = ['LoanStats3a.csv.zip', 'LoanStats3b.csv.zip', 'LoanStats3c.csv.zip', 'LoanStats3d.csv.zip']
	for f in FILENAMES:
	    location = DIR + f
	    dataframes.append(pd.read_csv(location, skiprows=1))

	df = pd.concat(dataframes, axis=0, ignore_index=True)
	return df
        
def prepare_data (df):
    #Choose cols that correlate to defaulted loans, and create new dataframe from them
    df = df[FEATURES]
    
    #From the loan-status column, take only fully paid, default, and charged-off rows
    df = df[(df.loan_status == "Fully Paid") | (df.loan_status == "Default") | (df.loan_status == "Charged Off")]

    #map fully paid to 1, and both default and charged-off to 0
    df['loan_status'] = df['loan_status'].map({'Fully Paid':1, 'Default':0, 'Charged Off':0})
    
    #Apply one hot encoding to categorical variables, and keep encoding
    encoder = ce.one_hot.OneHotEncoder()
    df = encoder.fit_transform(df)
    
    #the dataset has NaN values, so replace them using ffill
    df = df.fillna(method='ffill')
    
    return df, encoder
    
    
def make_model (df):
    #Split the dataset into a train and test set
    X = df.drop('loan_status', axis=1)
    Y = df['loan_status']

    #Create Random Forest Classifier instance and fit it to the data
    random_forest = RandomForestClassifier(n_estimators=100)
    model = random_forest.fit(X, Y)
    return model
    
def getLCModel():
    df = read_in_data()
    prepared_df, encoder = prepare_data(df)
    model = make_model(prepared_df)
    return model, encoder

if __name__ == '__main__':
    print("Kinetica Peer-to-Peer Lending Automated Underwriting Model")

    print("Training model...")
    #create the model based on past data
    model, encoder = getLCModel()

    print("Persisting trained model...")
    model_file = 'LC_model.sav'
    encoder_file = 'LC_encoder.sav'

    #Persist the model as bit dump
    pickle.dump(model, open(model_file, 'wb'))
    pickle.dump(encoder, open(encoder_file, 'wb'))
    print("Complete")
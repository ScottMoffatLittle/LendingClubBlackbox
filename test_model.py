import requests
import configparser
import json
from  bb_module_default import invest_or_not


sample_loan = {  
   "delinq2Yrs":0,
   "loanAmount":20000,
   "annualInc":80000.0,
   "homeOwnership":"MORTGAGE",
   "empLength":60,
   "ficoRangeHigh":680,
   "ficoRangeLow":670,
   "purpose":"credit_card",
   "dti":14,
   "grade":"B"
}

test_loan = sample_loan.copy()
print("Testing Fico Correlation:")
test_loan['ficoRangeHigh'] = 505
test_loan['ficoRangeHigh'] = 495
for i in range(12):
    test_loan['ficoRangeHigh'] = test_loan['ficoRangeHigh'] + 20
    test_loan['ficoRangeLow'] = test_loan['ficoRangeLow'] + 20

    print("    Fico score: " + str(test_loan['ficoRangeHigh'] - 5) + "           " + str(invest_or_not(test_loan)))

test_loan = sample_loan.copy()
print("Testing Grade Correlation:")
GRADES = ['G', 'F', 'E', 'D', 'C', 'B', 'A']
for grade in GRADES:
    test_loan['grade'] = grade
    print("    Grade: " + grade + "                  " + str(invest_or_not(test_loan)))

test_loan = sample_loan.copy()
print("Testing Income Correlation Correlation:")
test_loan['annualInc'] = 30000.0
for i in range(15):
    test_loan['annualInc'] = test_loan['annualInc'] + 10000.0
    print("    Annual Income: " + str(test_loan['annualInc']) + "    " + str(invest_or_not(test_loan)))

test_loan = sample_loan.copy()
print("Testing Home Ownership Correlation:")
test_loan['homeOwnership'] = "MORTGAGE"
print("    Home Ownership: " + "MORTGAGE" + "  " + str(invest_or_not(test_loan)))

test_loan['homeOwnership'] = 'RENT'
print("    Home Ownership: " + 'RENT' + "      " + str(invest_or_not(test_loan)))

test_loan['homeOwnership'] = "OWN"
print("    Home Ownership: " + "OWN" + "       " + str(invest_or_not(test_loan)))

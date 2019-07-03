
### Kinetica Machine Learning BlackBox Container SDK Sample
# __Automated Loan Underwriting for Peer-to-Peer Lending__
### by Scott Little, Julian Jenkins, Saif Ahmed
### Copyright (c) 2019 Kinetica DB Inc.
#### For support: support@kinetica.com

![Kinetica Logo](https://kinetica.s3.amazonaws.com/icon_p2p.png)


### Background

Our model was trained on the full history of LendingClub loan performance data (https://www.lendingclub.com/info/download-data.action) and utilizes RandomForest, SVM, and Logistic Regression Models to greenlight loans for investment.

### Usage

Our model can be used stand-alone or within Kinetica Active Analytics Workbench. The model implements the Kinetica BlackBox SDK r7.0.5 to enable highly resilient operations for the underwriting service.
For platform details, see the QuickStart at https://www.kinetica.com/tutorial/ml-powered-analytics/
Our model can inference against live loans from LendingClub using the Listed Loans API at https://api.lendingclub.com/api/investor/[version]/loans/listing
Details at: https://www.lendingclub.com/developers/listed-loans


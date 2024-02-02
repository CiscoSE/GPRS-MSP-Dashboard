GPRS-MSP-Dashboard

This repository will hold the code for the MSP Dashboard : https://charts.mongodb.com/charts-global-msp-noc-vktwd/public/dashboards/643d02a2-33ac-4db0-82cc-1e76be904285

![242937219-bef22c53-412a-44d0-8dbe-48d87e9d66ab](https://github.com/joeljos/GPRS-MSP-Dashboard/assets/11584709/d41bad5b-7006-4eee-8067-43b88c15bb06)

This is a Cross-Domain dashboard for displaying day 2 operations data from the Cisco Controllers. The final output is as shown in the chart above.

The sample of the dataset is given in demodbdata.py. You can take a look and see if it suits your requirement. If any data point that you are looking for in this scenario is not present, let us know by creating an issue for it in this repository.

You will need to create a credentials.py file as it is imported by most modules and the credentials are read from it. It has been added in .gitignore so that it wont be pushed into git from your local machine.

The initial step would be to ensure that the individual modules are working before trying to run the whole stack. The main files for initial testing are :
1) DNAC - Dnac_auth.py
2) vManage - vManage_auth.py
3) ThousandEyes - thousandEyes_auth.py

When you run the above files individually, you should be seeing a positive output with the data. Once this is achieved you can go to the remaining steps as described below.


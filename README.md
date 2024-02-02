GPRS-MSP-Dashboard

This repository will hold the code for the MSP Dashboard : https://charts.mongodb.com/charts-global-msp-noc-vktwd/public/dashboards/9aaa143d-2ec9-44a1-a4e2-44dee0a18c64 

![242937219-bef22c53-412a-44d0-8dbe-48d87e9d66ab](https://github.com/joeljos/GPRS-MSP-Dashboard/assets/11584709/d41bad5b-7006-4eee-8067-43b88c15bb06)

This is a Cross-Domain dashboard for displaying day 2 operations data from the Cisco Controllers. The final output is as shown in the chart above.

Outcome #1 : 
Multi Domain Dashboard with Catalyst Centre, Catalyst SDWAN and ThousandEyes

Note : The steps here are only for a lab environment. There may be additional considerations like security, performance, scalability, maintainability..etc needed before production use.

1.	Introduce the outcome and get hands-on experience with the creation of the dashboard
2.	Clone the GitHub repo, understand the code structure, architecture 
and API used
3.	Create Mongodb credentials
a.	In the Left panel, under Security category: 
i.	In the Network Access, enable allow all traffic
ii.	In the Database Access, create a new user (default user may not work) and save the password separately (as it will be needed later)
b.	In the Left panel, under Deployment category, go to :
i.	Database and then go to connect
ii.	Take Drivers
iii.	In step 3 there is a mongodb uri mentioned similar to “mongodb+srv://<username>:<password>@noc.5i3t1qh.mongodb.net/?retryWrites=true&w=majority”. Copy it and substitute with the username and password as obtained in 3.a.ii

4.	Update credential_sample.py (rename the file to credentials.py) with mongodb credentials as obtained in 3.b.iii in the variable “mongodb_uri”
5.	Execute the ControllerREST.py and drydbPush.py in the same order to observe how the data is returned from the Controllers. Now execute dbPush.py to observe how objects are created and populated in the mongodb instance
6.	In Mongodb, go to Deployment > Database in left panel and then towards “Browse Collections”. Under maindb collection, see the various data populated by the dbPush.py that was executed previously
7.	As a final step, go on and try to create the front-end using mongodb charts

![image](https://github.com/CiscoSE/GPRS-MSP-Dashboard/assets/11584709/b567a491-f71c-4995-84cf-792394829b46)



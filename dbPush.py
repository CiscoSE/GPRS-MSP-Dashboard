"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

import mongodb_auth
import requests
from pprint import pprint
import thousandEyesAppHealth
import dbnotifications


def runme():
    """This function is used to push data to the database
    parameters: None
    returns: None
    """
    db = mongodb_auth.authenticatedb()

    response = requests.get("http://10.1.8.29:5555/data")
    data = response.json()["data"]

    dbnotifications.runme(dataparam=data)

    vManageHealth_data = data["vManageHealth"]
    DnacHealth_data = data["DnacHealth"]
    vManageNWPI_readTrace_sloDetails = data["vManageNWPI_readTrace"][0]
    vManageNWPIAppHealth_data = data["vManageNWPI_readTrace"][1]
    DnacAppHealth_data = data["DnacAppHealth"]
    thousandEyesAppHealth_data = thousandEyesAppHealth.get_data()
    if(vManageNWPIAppHealth_data==[] and DnacAppHealth_data==[] and vManageNWPI_readTrace_sloDetails==[]):
        vManageNWPIAppHealth_data = [{"health":"green","name":"all","events":["positive"]}]
    tmp = {}
    result = int(vManageHealth_data[0]["networkHealth"]) * int(DnacHealth_data[0]["networkHealth"])
    if(result == 0):
        tmp["NetworkHealth"] = "critical"
    elif(result == -1):
        tmp["NetworkHealth"] = "moderate"
    else:
        tmp["NetworkHealth"] = "positive"    
    vManageAlarms_data = data["vManageAlarms"]
    DnacAlarms_data = data["DnacAlarms"]
   
    
    collection = db['NetworkHealth']
    print(mongodb_auth.purge_collection(collection))
    data = [tmp]
    print(mongodb_auth.addData(data,collection))

    collection = db['DeviceHealth']
    print(mongodb_auth.purge_collection(collection))
    data = vManageHealth_data[1]
    print(mongodb_auth.addData(data,collection))
    data = DnacHealth_data[1]
    print(mongodb_auth.addData(data,collection))

    collection = db['ApplicationHealth']
    print(mongodb_auth.purge_collection(collection))
    data = vManageNWPIAppHealth_data
    print(mongodb_auth.addData(data,collection))
    data = vManageNWPI_readTrace_sloDetails
    if(data!=[]):
        print(mongodb_auth.addData(data,collection))
    data = DnacAppHealth_data
    if(data!=[]):
        print(mongodb_auth.addData(data,collection))
    data = thousandEyesAppHealth_data
    if(data!=[]):
        print(mongodb_auth.addData(data,collection))
    
    if(vManageAlarms_data==[] and  DnacAlarms_data==[]):
        vManageAlarms_data = {"severity":"positive"}
    collection = db['Alarms']
    print(mongodb_auth.purge_collection(collection))
    data = vManageAlarms_data
    print(mongodb_auth.addData(data,collection))
    data = DnacAlarms_data
    if(data!=[]):
        print(mongodb_auth.addData(data,collection))

        

if __name__ == "__main__":
    runme()


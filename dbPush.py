import mongodb_auth
import requests
from pprint import pprint
import thousandEyesAppHealth
import dbnotifications


def runme():
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

        
runme()



"""

while(True):
    runme()
    print("Sleeping for 5 minutes..")
    time.sleep(300)

 """

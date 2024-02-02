import mongodb_auth
import requests
from pprint import pprint
import thousandEyesAppHealth
#import dbnotifications


def runme():
    """This function is used to push data to the database
    parameters: None
    returns: None
    """
    db = mongodb_auth.authenticatedb()

    response = requests.get("http://192.168.29.227:5555/data")
    data = response.json()["data"]
    print("completed getting data from ControllerREST..")

    #dbnotifications.runme(dataparam=data)

    vManageHealth_data = data["vManageHealth"]


    DnacHealth_data = data["DnacHealth"]
    vManageNWPI_readTrace_sloDetails = data["vManageNWPI_readTrace"][0]
    vManageNWPIAppHealth_data = data["vManageNWPI_readTrace"][1]
    DnacAppHealth_data = data["DnacAppHealth"]
    thousandEyesAppHealth_data = thousandEyesAppHealth.get_data()
    AppHealth_data = vManageNWPIAppHealth_data
    if(vManageNWPIAppHealth_data==[] and DnacAppHealth_data==[] and vManageNWPI_readTrace_sloDetails==[]):
        AppHealth_data = [{"health":"green","name":"all","events":["positive"]}]
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
    print("NetworkHealth : ",mongodb_auth.purge_collection(collection))
    data = [tmp]
    print("Added",mongodb_auth.addData(data,collection),"documents to collection.")

    collection = db['DeviceHealth']
    print("DeviceHealth : ",mongodb_auth.purge_collection(collection))
    data = vManageHealth_data[1]
    print("Added",mongodb_auth.addData(data,collection),"documents to collection.")
    data = DnacHealth_data[1]
    print("Added",mongodb_auth.addData(data,collection),"documents to collection.")

    collection = db['ApplicationHealth']
    print("ApplicationHealth : ", mongodb_auth.purge_collection(collection))
    data = AppHealth_data
    if(data!=[]):
        print("Added",mongodb_auth.addData(data,collection),"documents to collection.")
    data = vManageNWPI_readTrace_sloDetails
    if(data!=[]):
        print("Added",mongodb_auth.addData(data,collection),"documents to collection.")
    data = DnacAppHealth_data
    if(data!=[]):
        print("Added",mongodb_auth.addData(data,collection),"documents to collection.")
    data = thousandEyesAppHealth_data
    if(data!=[]):
        print(mongodb_auth.addData(data,collection))
    
    if(vManageAlarms_data==[] and  DnacAlarms_data==[]):
        DnacAlarms_data = {"severity":"positive"}
    collection = db['Alarms']
    print("Alarms : ", mongodb_auth.purge_collection(collection))
    data = DnacAlarms_data
    if(data!=[]):
        print("Added",mongodb_auth.addData(data,collection),"documents to collection.")
    data = vManageAlarms_data
    if(data!=[]):
        print("Added",mongodb_auth.addData(data,collection),"documents to collection.")
        

if __name__ == "__main__":
    runme()


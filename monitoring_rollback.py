from pprint import pprint

import requests

import credentials
import demodbdata
import mongodb_auth
import thousandEyesAppHealth

data =[]
db = []

def compare_alarm():
    """ Compares the alarms from vManage and DNAC and returns the summary and details of the comparison 
    parameters: None
    returns: [alarm_summary, alarm_details]
    """
    removed = []
    changed = []
    added = []
    same=[]    
    vManageAlarms_data = data["vManageAlarms"]
    DnacAlarms_data = data["DnacAlarms"]
    new_alarms = vManageAlarms_data.copy() + DnacAlarms_data.copy()
    collection = db['Alarms']
    old_data = collection.find()
    for item in old_data:
        count = 0
        for item2 in new_alarms:
            if(item["name"]==item2["name"] and item["summary"]==item2["summary"]):
                if(item["severity"]==item2["severity"]):
                    del item["_id"]
                    same.append(item.copy())
                    del item
                    new_alarms.remove(item2)
                    break
                else:
                    del item["_id"]
                    changed.append([item.copy(),item2.copy()])
                    del item
                    new_alarms.remove(item2)
                    break
            elif(item["name"]!=item2["name"] or item["summary"]!=item2["summary"] ):
                count+=1
                if(count==len(new_alarms)):
                    del item["_id"]
                    removed.append(item.copy())
                    del item
                    break

    added = new_alarms

    alarm_summary = {
        "changed":len(changed),
        "added":len(added),
        "removed":len(removed),
        "same":len(same),
        "total":len(changed)+len(added)+len(same)
    }
    alarm_details = {
        "changed":changed,
        "added":added,
        "removed":removed,
        "same":same,
        "total":changed + added + same
    }
    return [alarm_summary, alarm_details]


def compare_networkhealth():
    """ Compares the network health from vManage and DNAC and returns the summary and details of the comparison
    parameters: None
    returns: [networkhealth_summary, networkhealth_details]
    """
    removed = []
    changed = []
    added = []
    same=[]
    vManageHealth_data = data["vManageHealth"] 
    DnacHealth_data = data["DnacHealth"]
    tmp = {}
    result = int(vManageHealth_data[0]["networkHealth"]) * int(DnacHealth_data[0]["networkHealth"])
    if(result == 0):
        tmp["NetworkHealth"] = "critical"
    elif(result == -1):
        tmp["NetworkHealth"] = "moderate"
    else:
        tmp["NetworkHealth"] = "positive"  
    newdata = [tmp].copy()
    collection = db['NetworkHealth']
    olddata = collection.find()
    olddata = list(olddata)
    if(olddata==[]):
        olddata = [{"NetworkHealth":"No Data", "_id":"nodata"}]
    for item in olddata:
        for item2 in newdata:
            if(item["NetworkHealth"]==item2["NetworkHealth"]):
                del item["_id"]
                same.append(item.copy())
                del item
                newdata.remove(item2)
                break
            else:
                del item["_id"]
                changed.append([item.copy(),item2.copy()])
                del item
                newdata.remove(item2)
                break
    networkhealth_summary = {
        "changed":len(changed),
        "added":0,
        "removed":0,
        "same":len(same),
        "total":len(changed)+len(added)+len(same)
    }
    networkhealth_details = {
        "changed":changed,
        "added":[],
        "removed":[],
        "same":same,
        "total":changed + added + same
    }
    return [networkhealth_summary, networkhealth_details]


def compare_devicehealth():
    """ Compares the device health from vManage and DNAC and returns the summary and details of the comparison
    parameters: None
    returns: [devicehealth_summary, devicehealth_details]
    """

    removed = []
    changed = []
    added = []
    same=[]
    vManageHealth_data = data["vManageHealth"][1]
    DnacHealth_data = data["DnacHealth"][1]
    newdata = vManageHealth_data.copy() + DnacHealth_data.copy()
    collection = db['DeviceHealth']
    olddata = collection.find()
    for item in olddata:
        count = 0
        for item2 in newdata:
            if(item["url"]==item2["url"]):
                if(item["deviceHealth"]==item2["deviceHealth"]):
                    del item["_id"]
                    same.append(item.copy())
                    del item
                    newdata.remove(item2)
                    break
                else:
                    del item["_id"]
                    changed.append([item.copy(),item2.copy()])
                    del item
                    newdata.remove(item2)
                    break
            elif(item["url"]!=item2["url"]):
                count+=1
                if(count==len(newdata)):
                    del item["_id"]
                    removed.append(item.copy())
                    del item
                    break
    added = newdata
    devicehealth_summary = {
        "changed":len(changed),
        "added":len(added),
        "removed":len(removed),
        "same":len(same),
        "total":len(changed)+len(added)+len(same)
    }
    devicehealth_details = {
        "changed":changed,
        "added":added,
        "removed":removed,
        "same":same,
        "total":changed + added + same
    }
    return [devicehealth_summary, devicehealth_details]



def compare_applicationhealth():
    """ Compares the application health from vManage, DNAC and ThousandEyes and returns the summary and details of the comparison
    parameters: None
    returns: [applicationhealth_summary, applicationhealth_details]
    """
    
    removed = []
    changed = []
    added = []
    same=[]
    vManageNWPI_readTrace_sloDetails = data["vManageNWPI_readTrace"][0]
    vManageNWPIAppHealth_data = data["vManageNWPI_readTrace"][1]
    DnacAppHealth_data = data["DnacAppHealth"]
    thousandEyesAppHealth_data = thousandEyesAppHealth.get_data()
    if(vManageNWPIAppHealth_data==[] and DnacAppHealth_data==[] and vManageNWPI_readTrace_sloDetails==[]):
        vManageNWPIAppHealth_data = [{"health":"green","name":"all","events":["positive"]}]
    newdata = vManageNWPI_readTrace_sloDetails.copy()+vManageNWPIAppHealth_data.copy()+DnacAppHealth_data.copy()+thousandEyesAppHealth_data.copy()
    collection = db['ApplicationHealth']
    olddata = collection.find()
    for item in olddata:
        count = 0
        for item2 in newdata:
            if(item["name"]==item2["name"] and item["events"]==item2["events"] and item["url"]==item2["url"]):
                if(item["health"]==item2["health"]):
                    del item["_id"]
                    same.append(item.copy())
                    del item
                    newdata.remove(item2)
                    break
                else:
                    del item["_id"]
                    changed.append([item.copy(),item2.copy()])
                    del item
                    newdata.remove(item2)
                    break
            elif(item["name"]!=item2["name"] or item["events"]!=item2["events"] and item["url"]!=item2["url"]):
                count+=1
                if(count==len(newdata)):
                    del item["_id"]
                    removed.append(item.copy())
                    del item
                    break
    added = newdata
    applicationhealth_summary = {
        "changed":len(changed),
        "added":len(added),
        "removed":len(removed),
        "same":len(same),
        "total":len(changed)+len(added)+len(same)
    }
    applicationhealth_details = {
        "changed":changed,
        "added":added,
        "removed":removed,
        "same":same,
        "total":changed + added + same
    }
    return [applicationhealth_summary, applicationhealth_details]


def messageme(text):
    """ Sends a message to the user on webex teams
    parameters: text
    returns: None
    """

    header = {"Content-Type":"application/json", "Authorization":"Bearer "+credentials.webex_token}
    roomId="Y2lzY29zcGFyazovL3VzL1JPT00vYjc3ZjFhYTAtZDQ4Ni0xMWVkLThjOTgtMGIyNDQ4YjZmYzU4"
    body = {"roomId": roomId,"markdown":text}
    status = requests.post(url="https://webexapis.com/v1/messages",headers=header,json=body)
    if(status.status_code==200):
        pprint(status.json()["text"])
    else:
        print("some error trying to send webex message..",status)

def notify(intro,id,summary):
    """ Sends a message to the user on webex teams
    parameters: intro,id,summary
    returns: None
    """

    text = intro+" id : " + str(id)
    messageme(text=text)
    text = "**"+intro+"**"+" summary : "+str(summary)
    messageme(text=text)


def runme(dbparam,dataparam):
    """ Runs the script and sends the summary and details to the user on webex teams
    parameters: dbparam,dataparam
    returns: None
    """
    if(dbparam==None):
        dbparam = mongodb_auth.authenticatedb(dbname='storedb')
    if(dataparam==None):
        dataparam = demodbdata.data.copy()
    global data, db
    db = dbparam
    data = dataparam
    text = "**Cross-domain NOC for MSPs** : https://charts.mongodb.com/charts-global-msp-noc-vktwd/public/dashboards/643d02a2-33ac-4db0-82cc-1e76be904285"
    messageme(text=text)
    collection = db['store']
    summary, details = compare_alarm()
    print(mongodb_auth.purge_collection(collection))
    mdata = {"alarm_summary":summary.copy(),"alarm_details":details.copy()}
    id = collection.insert_one(mdata).inserted_id
    notify(intro="Alarm",id=id,summary=summary)
    summary, details = compare_networkhealth()
    print(mongodb_auth.purge_collection(collection))
    mdata = {"network_health_summary":summary.copy(),"network_health_details":details.copy()}
    id = collection.insert_one(mdata).inserted_id
    notify(intro="Network Health",id=id,summary=summary)
    summary, details = compare_devicehealth()
    print(mongodb_auth.purge_collection(collection))
    mdata = {"device_health_summary":summary.copy(),"device_health_details":details.copy()}
    id = collection.insert_one(mdata).inserted_id
    notify(intro="Devices Health",id=id,summary=summary)
    summary, details = compare_applicationhealth()
    print(mongodb_auth.purge_collection(collection))
    mdata = {"application_health_summary":summary.copy(),"application_health_details":details.copy()}
    id = collection.insert_one(mdata).inserted_id
    notify(intro="Application Health",id=id,summary=summary)



if __name__ == "__main__":
    runme()
    
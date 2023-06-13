import thousandEyes_auth
from pprint import pprint

testids=['3732333']

def get_data():
    apphealth=[]
    for item in testids:
        data = thousandEyes_auth.get_data(uri="/v6/web/http-server/"+item)['web']['httpServer'][0]
        if(data["errorType"]!="None"):
            apphealth.append({"health":"critical","name":"TE agent: "+data["agentName"],"events":data["errorDetails"],"url":data["permalink"]})
    return apphealth

if __name__ == "__main__":
    pprint(get_data())

import requests
from pprint import pprint
import time
import dbnotifications



def runme():
    response = requests.get("http://10.1.8.29:5555/data")
    if response.status_code ==200:
        data = response.json()["data"]
        dbnotifications.runme(dataparam=data)
    else:
        return response
    return data



if __name__ == '__main__':
    count = 0
    while(True):
        try:
            pprint(runme())
        except Exception as e:
            print("Exception occured : ",e)
            print("Continuing..")
            continue
        count+=1
        print("dryrun count is : ",count,"\nSleeping for 60 seconds..")
        time.sleep(60)
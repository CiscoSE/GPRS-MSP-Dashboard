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

import Dnac_auth
from pprint import pprint



def get_networkhealth():
    returnData = {}
    data = Dnac_auth.get_data(uri="/dna/intent/api/v1/network-health")['response'][0]
    if(data["healthScore"]>99):
        returnData['networkHealth'] = 1
    elif(data["healthScore"]>0 and data["healthScore"]<100 ):
        returnData['networkHealth'] = -1
    else:
        returnData['networkHealth'] = 0
    return returnData


def get_devicehealth():
    itemData = {}
    returnData = []
    data = Dnac_auth.get_data(uri="/dna/intent/api/v1/device-health")['response']
    for item in data:
        itemData["name"] = item["name"]
        itemData["deviceFamily"] = item["deviceFamily"].lower()
        itemData["reachabilityHealth"] = item["reachabilityHealth"].lower()
        itemData["ipAddress"] = item["ipAddress"]
        if(item["overallHealth"]>9):
            itemData['deviceHealth'] = "positive"
        elif(item["overallHealth"]>0 and item["overallHealth"]<10):
            itemData['deviceHealth'] = "moderate"
        else:
            itemData['deviceHealth'] = "critical"
        query = {
            "searchBy": item["macAddress"],
            "identifier": "macAddress"
        }
        detailData = Dnac_auth.get_data(uri="/dna/intent/api/v1/device-detail", query=query)['response']
        itemData['url'] = Dnac_auth.BASE_URL + "/dna/assurance/device/details?id=" + detailData["nwDeviceId"]
        itemData["uuid"] = detailData["nwDeviceId"]
        returnData.append(itemData.copy())
    return returnData

def get_platformhealth():
    data = Dnac_auth.get_data(uri="/dna/intent/api/v1/diagnostics/system/health")
    pprint(data)

    


def get_data():
    data = [get_networkhealth(), get_devicehealth()]
    return data    


        


if __name__ == "__main__":
    pprint(get_data())

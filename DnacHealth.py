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

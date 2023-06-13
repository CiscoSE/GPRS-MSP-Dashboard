import Dnac_auth
from pprint import pprint

def get_clientHealth():
   data = Dnac_auth.get_data(uri="/dna/intent/api/v1/device-health")['response']
   for item in data:
        query = {
            "searchBy": item["macAddress"],
            "identifier": "macAddress"
        }
        detailData = Dnac_auth.get_data(uri="/dna/intent/api/v1/device-detail", query=query)['response']
        query = {
            "deviceId": detailData["nwDeviceId"]
        }
        tmp = Dnac_auth.get_data(uri="/dna/intent/api/v1/application-health", query=query)['response']
        pprint(query)
        for item2 in tmp:
            pprint(item2)

        



if __name__ == "__main__":
    pprint(get_clientHealth())
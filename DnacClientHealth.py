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